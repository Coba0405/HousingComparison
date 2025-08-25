const BASE = 'http://lacalhost:8000'

export async function simulateRent(payload) {
    const r = await fetch(`${BASE}/simulate/rent`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    })
    return r.json()
}
export async function simulateHouse(payload) {
    const r = await fetch(`${BASE}/simulate/house`, {
        mothod: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    })
    return r.json()
}
export async function simulateCondo(payload) {
    const r = await fetch(`${BASE}/simulate/condo`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    })
    return r.json()
}
