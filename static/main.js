let copied_once = false;

function get_table_heading_text() {
  let cells = document.querySelectorAll("#data thead tr th:not(.control)");
  let res = [];
  cells.forEach((c) => {
    res.push(c.innerHTML);
  });
  return res.join("\t");
}

function get_table_rows() {
  return document.querySelectorAll("#data tbody tr:not(.disabled)");
}

function get_row_text(tr) {
  const cells = tr.querySelectorAll("input:not(.toggle)");
  let res = [];
  cells.forEach((c) => {
    val = c.value;
    if (c.classList.contains("accuracy")) {
      val += " m";
    }
    res.push(val);
  });
  return res.join("\t");
}

function get_table_text() {
  let res = [get_table_heading_text()];

  let rows = get_table_rows();
  rows.forEach((row) => {
    res.push(get_row_text(row));
  });
  return res.join("\n");
}

function add_options_to_list(list_id, data) {
  const data_list = document.getElementById(list_id);
  const tpl = document.getElementById("option-template");
  data.forEach((element) => {
    const words = element.split(" ");
    for (let i = 0; i < words.length; i++) {
      words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }
    const opt = document.createElement("option");
    opt.setAttribute("value", words.join(" "));
    opt.innerHTML = "";
    data_list.appendChild(opt);
  });
}

function validate_species(el) {
  if (dictionary.includes(el.value.toLowerCase())) {
    el.parentNode.classList.remove("danger");
  } else {
    el.parentNode.classList.add("danger");
  }
}

function init_results() {
  if (document.querySelector(".error") != null) {
    console.log(document.querySelector(".error"))
    return;
  }

  copied_once = false;
  const species_inputs = document.querySelectorAll("input.species");
  add_options_to_list("species_list", dictionary);
  species_inputs.forEach((el) => {
    validate_species(el);
    el.addEventListener("input", (e) => {
      validate_species(e.target);
    });
  });

  const copy_button = document.getElementById("copy");
  const copy_message = document.getElementById("copy-msg");
  if (copy_button != null) {
    copy_button.addEventListener("click", (e) => {
      let txt = get_table_text();
      navigator.clipboard.writeText(txt);
      copy_button.classList.replace("fa-copy", "fa-thumbs-o-up");
      copy_button.classList.add("secondary");
      copy_message.innerHTML = "Kopierat!"
      let step6 = document.querySelector("#step6");
      if(step6 != null) {
        step6.classList.remove("hidden");
      }
      copied_once = true;
    });
  }

  function reset_copy_button() {
    if(copied_once){
      copy_button.classList.replace("fa-thumbs-o-up", "fa-copy");
      copy_button.classList.remove("secondary");
      copy_message.innerHTML = "Kopiera";
    }
  }

  const all_inputs = document.querySelectorAll("#data input");
  all_inputs.forEach((el) => {
    el.addEventListener("input", (e) => {
      reset_copy_button();
    });
  });

  const toggles = document.querySelectorAll(".toggle");
  toggles.forEach((button) => {
    button.addEventListener("input", (e) => {
      if (e.target.checked) {
        e.target.parentNode.parentNode.classList.remove("disabled");
      } else {
        e.target.parentNode.parentNode.classList.add("disabled");
      }
    });
  });

  const ap_link = document.getElementById("ap-link");
  if (ap_link != null) {
    ap_link.addEventListener("click", (e) => {
      document.getElementById("easter-egg").classList.remove("hidden");
    })
  }

}

document.addEventListener("htmx:afterSettle", (e) => {
  console.log(e);
  init_results();
});
