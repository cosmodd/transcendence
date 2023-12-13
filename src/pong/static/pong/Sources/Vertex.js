import { Vec3 } from "./Vector.js";

class Vertex {
    // constructor(position = null, normal = null, texCoords = null, color = null) {
    constructor(position = null, color = null) {
        this.position = position || new Vec2();
        // this.normal = normal || new Vec3;
        // this.texCoords = texCoords || new Vec2;
        this.color = color || new Vec3();
    }

    toArray() {
        return [...this.position.toArray(), ...this.color.toArray()]
    }
}

export default Vertex;
