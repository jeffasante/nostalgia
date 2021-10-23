

const jsArrayOfItems = {{title_list | tojson | safe}};
console.log(jsArrayOfItems)
// console.log({{ title_list[:5]|saf }})


// function filterFunc(){
//     let input, filter, a;

//     input = document.getElementById('myInput');
//     filter = input.value.toUpperCase();
//     div = document.getElementById('myDropdown');


    // a = div.getElementsByTagName('a');
    // var geocode = '{{ title_list[:5]|tojson }}'
    // console.log({{ title_list[:5]|tojson }})
    // // console.log(a[0].textContent);
    // for (let i=0; i < a.length; i++) {
    //     txtVal = a[i].textContent || a[i].innerText;
    //     if (txtVal.toUpperCase().indexOf(filter) > -1) {
    //      a[i].style.display = "";
    //     } else {
    //     a[i].style.display = "none";
    //     }

    // }

// }
