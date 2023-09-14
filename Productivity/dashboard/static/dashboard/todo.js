document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.delete').forEach(button => {
        button.addEventListener('click', ()=>{
            const task = (button.parentElement).parentElement;
            task.className = "alert alert-danger"
            task.style.display = "none";
            console.log(task);
            event.preventDefault();
            fetch(`/todo/${task.id}`, {
                method:'DELETE',
            })
            document.querySelector("#count").innerHTML = parseInt(document.querySelector("#count").innerHTML) - 1
        })
    });

    document.querySelectorAll('.undo').forEach(button => {
        button.addEventListener('click', ()=>{
            const task = (button.parentElement).parentElement;
            task.className = "alert alert-success"
            task.style.display = "none";
            event.preventDefault();
            console.log(task)
            fetch(`${task.id}`, {
                method:'PUT',
            })
            document.querySelector("#count").innerHTML = parseInt(document.querySelector("#count").innerHTML) - 1
        });
    });

    document.querySelectorAll('.completed').forEach(button => {
        button.addEventListener('click', ()=>{
            const task = (button.parentElement).parentElement;
            task.className = "alert alert-success"
            task.style.display = "none";
            event.preventDefault();
            fetch(`todo/${task.id}`, {
                method:'PUT',
            })
            document.querySelector("#count").innerHTML = parseInt(document.querySelector("#count").innerHTML) - 1
        });
    });

    document.querySelectorAll('.edit').forEach(button => {
        button.addEventListener('click', ()=>{
            const task = (button.parentElement).parentElement;
            task.querySelector(".standard-view").style.display="none";
            task.querySelector(".edit_data").style.display="block";
        })
    });

    document.querySelectorAll('.resave').forEach(value => {
        value.addEventListener('click', async function (event) {
            const button = event.target;
            const form = button.parentElement;
            const task = form.parentElement;
            event.preventDefault();
            fetch(`/todo/${task.id}`, {
                method: 'POST',
                body: JSON.stringify({
                    name: form.querySelector("input[type=text]").value,
                    action: form.querySelector("textarea").value,
                })  
            })
            .then(async(response) => {
                task.querySelector(".standard-view").style.display = "block";
                form.style.display = "none";
                task.querySelector(".name").innerHTML = form.querySelector("input[type=text]").value;
                task.querySelector(".action").innerHTML = form.querySelector("textarea").value;
            });
        });
    });

    document.querySelectorAll(".create").forEach(button =>{
        button.addEventListener('click', ()=> {
        form = document.querySelector("#new")
        if (form.style.display == "none"){
            form.style.display = "block";
            document.querySelector("#task-list").style.filter = "blur(1.5px)"
        }
        else {
            form.style.display = "none";
            document.querySelector("#task-list").style.filter = "blur(0px)"
        }
        
        });
    });
    
});