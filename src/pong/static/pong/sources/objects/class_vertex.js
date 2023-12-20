import { Vec3 } from "../utils/class_vec.js";

class Vertex {
    // constructor(position = null, normal = null, texCoords = null, color = null) {
    constructor(position = null, color = null) {
        this.position = position || new Vec2();
        // this.normal = normal || new Vec3;
        // this.texCoords = texCoords || new Vec2;
        this.color = color || new Vec3();
    }

    ToArray() {
        return [...this.position.ToArray(), ...this.color.ToArray()]
    }
}

export default Vertex;
