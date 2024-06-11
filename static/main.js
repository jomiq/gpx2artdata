let clipboard = new ClipboardJS(".btn");
let copy_button = document.querySelector("#copy")
clipboard.on('success', function(e) {
  copy_button.innerHTML = "Kopierat!";
  copy_button.classList.add("secondary")
  e.clearSelection();
});

clipboard.on('error', function(e) {
  console.error('Action:', e.action);
  console.error('Trigger:', e.trigger);
});

let toggles = document.querySelectorAll('.toggle');

function reset_copy_button(){
  copy_button.classList.remove("secondary");
  copy_button.innerHTML = "Kopiera";
}

toggles.forEach(button => {
  button.addEventListener('click', function(e) {
    e.target.parentNode.parentNode.classList.toggle('unselectable');
    reset_copy_button();
  });
});


let species = document.querySelectorAll(".species")

function check_species(el) {
  if(dictionary.includes(el.innerHTML.lower())){
    el.classList.remove("danger");
  } else {
    el.classList.add("danger");
    }
}

document.addEventListener("DOMContentLoaded", (e) => {
  species.forEach(el => {
    check_species(el);
    el.addEventListener("input", (e) => {
      console.log(e)
      check_species(e.target);
      });
  });
});
