const cement = document.getElementById('cement')
const blastFurnace = document.getElementById('blastFurnace')
const flyAsh = document.getElementById('flyAsh')
const water = document.getElementById('water')
const superplastic = document.getElementById('superplastic')
const coarse = document.getElementById('coarse')
const fine = document.getElementById('fine')
const age = document.getElementById('age')

const predictBtn = document.getElementById('predict-btn')
const resultValue = document.querySelector('.result-value')

predictBtn.addEventListener('click', async function predict(e) {
   
    if (e) e.preventDefault()

    resultValue.innerHTML = "Calculating..."


    if (window.location.port === "5500" || window.location.protocol === "file:") {
        resultValue.innerHTML = "Port Error";
        alert("You MUST open http://127.0.0.1:8000 in your browser for the Python backend to connect.");
        return
    }

    const data = {
        cement: parseFloat(cement.value) || 0,
        blastFurnace: parseFloat(blastFurnace.value) || 0,
        flyAsh: parseFloat(flyAsh.value) || 0,
        water: parseFloat(water.value) || 0,
        superplastic: parseFloat(superplastic.value) || 0,
        coarse: coarse.value ? parseFloat(coarse.value) : 0,
        fine: fine.value ? parseFloat(fine.value) : 0,
        age: age.value ? parseFloat(age.value) : 0,
    }

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })

        if (!response.ok) {
            throw new Error(`HTTP ${response.status} - Backend rejected the request.`)
        }

        const result = await response.json()

        
        if (result.error) {
            console.error("Python Error:", result.error)
            resultValue.innerHTML = "Python Error"
            alert("Python crashed! Error: " + result.error)
        } else {
            resultValue.innerHTML = result.prediction.toFixed(2)
        }

    } catch (error) {

        console.error("Crash Details:", error)
        resultValue.innerHTML = "Error"
        alert("Is your Uvicorn server running in the terminal?")
    }
});