
const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value


const sendSearchData = (searchValue) => {
    $.ajax({
        type: 'POST',
        url: 'search',
        data: {
            'csrfmiddlewaretoken': csrf,
            'searchValue': searchValue, //game in the example
        },
        success: (response)=> { //response return as jason Respons from a view
            
            const data = response.data
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                data.forEach(searchValue=> {
                    resultsBox.innerHTML += `
                    <div style="justify-content: space-between; ; display: flex;"  class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
                        <div  class="btn-group me-2" role="group" aria-label="First group">  
                            
                            <option>${searchValue.product_name}</option>
                            
                        </div>
                            <div class="btn-group btn-group-sm" role="group" > 
                                <a class="btn btn-outline-success" href="/appointment/${searchValue.id}">view</a>
                            </div>
                        </div>
                    `
                })
            } else {
                if (searchInput.value.length > 0){
                    resultsBox.innerHTML = `<p>${data}</p>`
                }else {
                    resultsBox.classList.add('not-visible')
                }
            }
            
        },
        error: (error)=> {
            // console.log(error)
        }
    })


}


// by this any this tou type will be visible live
searchInput.addEventListener('keyup', e=> {
    // console.log(e.target.value)

    if (resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
    }
    sendSearchData(e.target.value)
})


// Get the <p> tag and input field
const changeValueP = document.getElementById('');
const inputField = document.getElementById('');

// Add click event listener to the <p> tag
changeValueP.addEventListener('click', () => {
    // Change the value of the input field
    inputField.value = changeValueP.value ;
    });


