export class Vec3 {
    constructor(x, y, z) {
        this.x = x || 0;
        this.y = y || 0;
        this.z = z || 0;
    }

    toArray() {
        return [this.x, this.y, this.z];
    }

    normalize() {
        const length = Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
        if (length !== 0) {
            this.x /= length;
            this.y /= length;
            this.z /= length;
        }
        return this;
    }

    clone() {
        return new Vec3(this.x, this.y, this.z);
    }

    multiplyScalar(scalar) {
        this.x *= scalar;
        this.y *= scalar;
        this.z *= scalar;
        return this;
    }

    add(v) {
        this.x += v.x;
        this.y += v.y;
        this.z += v.z;
        return this;
    }
}

export class Vec2 {
    constructor(x, y) {
        this.x = x || 0;
        this.y = y || 0;
    }

    toArray() {
        return [this.x, this.y];
    }

    normalize() {
        const length = Math.sqrt(this.x * this.x + this.y * this.y);
        if (length !== 0) {
            this.x /= length;
            this.y /= length;
        }
        return this;
    }

    clone() {
        return new Vec2(this.x, this.y);
    }

    multiplyScalar(scalar) {
        this.x *= scalar;
        this.y *= scalar;
        return this;
    }

    add(v) {
        this.x += v.x;
        this.y += v.y;
        return this;
    }
}