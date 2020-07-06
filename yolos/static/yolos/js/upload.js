const uploadButton = document.querySelector('#fileupload')
    uploadButton.addEventListener('change', function(event) {
        console.log(event)
        const imagefile = document.querySelector('#fileupload')
        const formData = new FormData();
        formData.append("image", imagefile.files[0]);
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.post('/yolos/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
              }
        })
        .then(response => {
            console.log(response)
            const imgTag = document.querySelector('#imgSrc')
            imgTag.src = response.data.img_url
            imgTag.style.height = '500px'
        })
        .catch(error => console.log(error))
    })
const searchButton = document.querySelector('#yolo')
    searchButton.addEventListener('click', function(event) {
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.post('/yolos/goflow/', {
            headers: {
                'Content-Type': 'multipart/form-data'
              }
        })
        .then(response => {
            console.log(response)
            const results = response.data.result
            console.log(result)
            // const resultDiv = document.querySelector('#result')
            // resultDiv.innerHTML = `
            //     <h1>${result.label}인듯</h1>
            //     <h2>${result.confidence*100}%!!!!</h2>
            // `
            document.querySelectorAll('.label').forEach( label => label.remove())
            document.querySelectorAll('.text').forEach( text => text.remove())
            document.querySelectorAll('.result-box').forEach(result => {result.remove()})
            results.forEach(function(result){
                // const resultLabel = document.querySelector('.label')
                const div = document.createElement('div')
                const textDiv = document.createElement('div')
                textDiv.className = 'result-box'
                textDiv.innerHTML = `
                <h1 class="result-text">${result.label}</h1>
                <h2 class="result-percent">${result.confidence*100}%</h2>
                `
                const x = result.bottomright.x - result.topleft.x
                const y = result.bottomright.y - result.topleft.y
                div.className = 'label'
                div.setAttribute('style', `position: absolute; width: ${x}px; height: ${y}px; top: ${result.topleft.y}px; left: ${result.topleft.x}px; border: 2px solid red; color: red; box-sizing: border-box;`)
                const resultImageDiv = document.querySelector('#result-image-div')
                resultImageDiv.appendChild(div)
                document.querySelector('#card-result').appendChild(textDiv)
    
                const resultTag = document.querySelector('#resultImg')
                resultTag.src = response.data.img_url
            })
            const show = document.querySelector('#resultCard')
            show.style.display = "block"
            window.scrollTo({ top: show.scrollHeight + 200, behavior: 'smooth' })
            
        })
        .catch(error => console.log(error))

    })