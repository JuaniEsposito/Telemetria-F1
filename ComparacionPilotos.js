// src/components/ComparacionPilotos.js
import React, { useState } from 'react';
import axios from 'axios';

function ComparacionPilotos() {
    const [data, setData] = useState(null);

    const handleClick = async () => {
        const res = await axios.get("http://localhost:8000/compare?driver1=VER&driver2=HAM");
        setData(res.data);
    };

    return (
        <div>
            <button onClick={handleClick}>Comparar VER vs HAM</button>
            {data && (
                <div>
                    <h2>Comparación de Vueltas</h2>
                    {/* Aquí puedes usar chart.js, recharts, etc. 
                        Ejemplo simple: */}
                    <pre>{JSON.stringify(data, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}
export default ComparacionPilotos;
