const BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

async function postJSON(path, payload) {
    const res = await fetch(`${BASE}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });
    if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(`HTTP ${res.status} ${res.statusText}: ${text}`);
    }
    return res.json();
}

export function simulateRent(payload) {
    return postJSON('/simulate/rent', payload);
}

export async function simulateOwner(payload) {
    return postJSON('/simulate/owner', payload);
}
export async function simulateCondo(payload) {
    return postJSON('/simulate/condo', payload);
}

export { BASE };
