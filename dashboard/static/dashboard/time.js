document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll(".create_alarm").forEach(button =>{
        button.addEventListener('click', ()=> {
            form = document.querySelector("#new")
            if (form.style.display == "none"){
                form.style.display = "block";
                document.querySelector("#alarms").style.filter = "blur(1.5px)"
            }
            else {
                form.style.display = "none";
                document.querySelector("#alarms").style.filter = "blur(0px)"
            }
        });
    });

    document.querySelectorAll('.delete').forEach(button => {
        button.addEventListener('click', ()=>{
            const alarm = (button.parentElement).parentElement;
            console.log(alarm.id)
            alarm.style.display = "none";
            event.preventDefault();
            fetch(`time/alarm/${alarm.id}`, {
                method:'DELETE',
            })
        })
    });

    fetch("time/alarm")
    .then(response => response.json())
    .then(values => {
        values.forEach(value => {
            var x = setInterval(function(){
                finalDate = new Date(`${value["date"]}`).getTime()/1000;
                var nowDate = new Date().getTime()/1000;
                distance =  finalDate - nowDate;

                var d = Math.floor(distance / (3600 * 24));
                var h = Math.floor((distance % (3600 * 24)) / (3600));
                var m = Math.floor((distance % (3600)) / (60));
                var s = Math.floor((distance % (60)));

                if (distance < 0){
                    alarm = document.querySelector(`#countdown-${value.id}`)
                    alarm.innerHTML = "<b>EXPIRED</b>";
                    alarm.parentElement.className = "alert alert-danger";
                    
                    fetch(`/time/alarm/${value.id}`, {
                        'method':'PUT'
                    })
                    clearInterval(x);
                    
                }
                else{
                    document.querySelector(`#countdown-${value.id}`).innerHTML = d + "d " + h + "h " + m + "m " + s + "s";
                }
            }, 1000) 
        });
    });
});
