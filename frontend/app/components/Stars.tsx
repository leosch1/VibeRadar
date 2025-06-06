import { useMemo } from "react";
import { Points, PointMaterial } from "@react-three/drei";

export function Stars({ count = 5000 }) {
    const positions = useMemo(() => {
        const pos = [];
        const minRadius = 500;
        const maxRadius = 1500;
        for (let i = 0; i < count; i++) {
            const theta = Math.random() * 2 * Math.PI;
            const phi = Math.acos(2 * Math.random() - 1);
            const radius = Math.random() * (maxRadius - minRadius) + minRadius;

            const x = radius * Math.sin(phi) * Math.cos(theta);
            const y = radius * Math.sin(phi) * Math.sin(theta);
            const z = radius * Math.cos(phi);

            pos.push(x, y, z);
        }
        return new Float32Array(pos);
    }, [count]);


    return (
        <Points positions={positions} frustumCulled={false}>
            <PointMaterial
                transparent
                color="#ffffff"
                size={3}
                sizeAttenuation={true}
                depthWrite={false}
            />
        </Points>
    );
}
