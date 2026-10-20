/** Offline 3D reference-sphere renderer by Jason Stys.
 * Class: OrbitScene owns disposable WebGL resources and bounded camera controls.
 * Variables: PALETTE, scene/camera/renderer/controls/markers. Index: docs/CODE_INDEX.md.
 */
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { atTime } from "./display";
import type { Run } from "./types";
export const PALETTE = ["#63e4da", "#ffc27a", "#b8a3ff"];

/** Rebuild one small scene per run; no global animation loop or remote textures. */
export class OrbitScene {
  private renderer: THREE.WebGLRenderer;
  private scene = new THREE.Scene();
  private camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
  private controls: OrbitControls;
  private markers: THREE.Mesh[] = [];
  private observer: ResizeObserver;
  constructor(
    private container: HTMLElement,
    private run: Run,
  ) {
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.domElement.setAttribute("aria-hidden", "true");
    container.append(this.renderer.domElement);
    this.camera.position.set(2.1, 1.5, 2.6);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.minDistance = 1.6;
    this.controls.maxDistance = 6;
    this.controls.enablePan = false;
    this.controls.addEventListener("change", () => this.draw());
    this.scene.add(new THREE.AmbientLight(0xb8dce8, 2));
    const light = new THREE.DirectionalLight(0xffffff, 2);
    light.position.set(3, 2, 4);
    this.scene.add(light);
    const sphere = new THREE.Mesh(
      new THREE.SphereGeometry(1, 48, 32),
      new THREE.MeshStandardMaterial({ color: 0x133b50, roughness: 0.8 }),
    );
    const grid = new THREE.Mesh(
      new THREE.SphereGeometry(1.002, 24, 12),
      new THREE.MeshBasicMaterial({
        color: 0x346a7a,
        wireframe: true,
        transparent: true,
        opacity: 0.25,
      }),
    );
    this.scene.add(sphere, grid);
    run.tracks.forEach((track, i) => {
      const points = track.samples.map((s) =>
        new THREE.Vector3(...s.position).divideScalar(run.earth_radius_km),
      );
      this.scene.add(
        new THREE.Line(
          new THREE.BufferGeometry().setFromPoints(points),
          new THREE.LineBasicMaterial({ color: PALETTE[i % PALETTE.length]! }),
        ),
      );
      const marker = new THREE.Mesh(
        new THREE.SphereGeometry(0.017, 12, 8),
        new THREE.MeshBasicMaterial({ color: PALETTE[i % PALETTE.length]! }),
      );
      this.scene.add(marker);
      this.markers.push(marker);
    });
    this.observer = new ResizeObserver(() => this.resize());
    this.observer.observe(container);
    this.resize();
    this.update(0);
  }
  /** Resize from actual container dimensions, including mobile and hidden-to-visible transitions. */
  private resize(): void {
    const width = Math.max(1, this.container.clientWidth),
      height = Math.max(1, this.container.clientHeight);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
    this.draw();
  }
  /** Reflect a bounded display offset; normalized coordinates retain equal axis scales. */
  update(time: number): void {
    this.run.tracks.forEach((track, i) => {
      const position = atTime(track, time).position;
      this.markers[i]!.position.set(...position).divideScalar(this.run.earth_radius_km);
    });
    this.draw();
  }
  /** Keyboard-accessible reset replaces pointer-only navigation. */
  reset(): void {
    this.camera.position.set(2.1, 1.5, 2.6);
    this.controls.target.set(0, 0, 0);
    this.controls.update();
    this.draw();
  }
  /** Render only when data or controls change, not a permanent GPU loop. */
  private draw(): void {
    this.renderer.render(this.scene, this.camera);
  }
  /** Release buffers, listeners, resize observation, canvas and renderer on scenario changes. */
  dispose(): void {
    this.observer.disconnect();
    this.controls.dispose();
    this.scene.traverse((object) => {
      if (object instanceof THREE.Mesh || object instanceof THREE.Line) {
        object.geometry.dispose();
        const materials = Array.isArray(object.material) ? object.material : [object.material];
        materials.forEach((material) => material.dispose());
      }
    });
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }
}
