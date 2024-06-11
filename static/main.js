function reset_copy_button() {
  const copy_button = document.getElementById("copy");
  copy_button.classList.remove("secondary");
  copy_button.innerHTML = "Kopiera";
}

function add_options_to_list(list_id, data) {
  const data_list = document.getElementById(list_id);
  const tpl = document.getElementById("option-template");
  data.forEach(element => {
    const words = element.split(" ");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }
    const opt = document.createElement("option")
    opt.setAttribute("value", words.join(" "))
    opt.innerHTML = ""
    data_list.appendChild(opt)
  });
}


function check_species(el) {
  if (dictionary.includes(el.value.toLowerCase())) {
    el.parentNode.classList.remove("danger");
  } else {
    el.parentNode.classList.add("danger");
  }
}


document.addEventListener("DOMContentLoaded", (e) => {
  const species_inputs = document.querySelectorAll("input.species");
  add_options_to_list("species_list", dictionary);
  species_inputs.forEach((el) => {
    check_species(el);
    el.addEventListener("input", (e) => {
      console.log(e);
      check_species(e.target);
    });
  });

  const toggles = document.querySelectorAll(".toggle");
  toggles.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.target.parentNode.parentNode.classList.toggle("disabled");
      reset_copy_button();
    });
  });
});
