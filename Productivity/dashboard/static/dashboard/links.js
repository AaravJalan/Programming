document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('.delete').forEach(button => {
        button.addEventListener('click', ()=>{
            const link = ((button.parentElement).parentElement).parentElement;;
            link.style.display = "none";
            event.preventDefault();
            fetch(`links/${link.id}`, {
                method:'DELETE',
            })
            document.querySelector("#count").innerHTML = parseInt(document.querySelector("#count").innerHTML) - 1
        })
    });

    document.querySelectorAll(".create").forEach(button =>{
        button.addEventListener('click', ()=> {
            form = document.querySelector("#new")
            if (form.style.display == "none"){
                form.style.display = "block";
                document.querySelector("#links-list").style.filter = "blur(1.5px)"
            }
            else {
                form.style.display = "none";
                document.querySelector("#links-list").style.filter = "blur(0px)"
            }
        }) 
    })
    
})