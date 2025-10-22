// src/components/EstrategiaPiloto.js
import React, { useState } from 'react';
import axios from 'axios';

function EstrategiaPiloto() {
    const [info, setInfo] = useState(null);

    const handleCargar = async () => {
        const res = await axios.get("http://localhost:8000/strategy?driver=VER");
        setInfo(res.data);
    };

    return (
        <div>
            <button onClick={handleCargar}>Ver Estrategia VER</button>
            {info && (
                <>
                    <h3>Stints</h3>
                    <pre>{JSON.stringify(info.stints, null, 2)}</pre>
                    <h3>Paradas en Boxes</h3>
                    <pre>{JSON.stringify(info.pitstops, null, 2)}</pre>
                </>
            )}
        </div>
    );
}
export default EstrategiaPiloto;
