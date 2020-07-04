const uploadButton = document.querySelector('#upload')
    uploadButton.addEventListener('click', function(event) {
        event.preventDefault()
        const imagefile = document.querySelector('#file')
        const formData = new FormData();
        formData.append("image", imagefile.files[0]);
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.post('/colorize/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
              }
        })
        .then(response => {
            console.log("-------------------------------")
            console.log(response)
            const imgTag = document.querySelector('#shoes-img')
            imgTag.src = response.data.img_url
            imgTag.style.height = '500px'
        })
        .catch(error => console.log(error))
    })

const uploadButton2 = document.querySelector('#shape-upload')
    uploadButton2.addEventListener('click', function(event) {
        event.preventDefault()
        const imagefile2 = document.querySelector('#shape-file')
        const formData2 = new FormData();
        formData2.append("image", imagefile2.files[0]);
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.post('/colorize/upload2/', formData2, {
            headers: {
                'Content-Type': 'multipart/form-data'
                }
        })
        .then(response => {
            console.log("-------------------------------")
            console.log(response)
            const imgTag2 = document.querySelector('#shape')
            imgTag2.src = response.data.img_url2
            imgTag2.style.height = '500px'
        })
        .catch(error => console.log(error))
    })


