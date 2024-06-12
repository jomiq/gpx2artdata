function get_table_heading_text() {
  let cells = document.querySelectorAll("#data thead tr td:not(.control)");
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
  const cells = tr.querySelectorAll("input");
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
  const species_inputs = document.querySelectorAll("input.species");
  add_options_to_list("species_list", dictionary);
  species_inputs.forEach((el) => {
    validate_species(el);
    el.addEventListener("input", (e) => {
      validate_species(e.target);
    });
  });

  const copy_button = document.getElementById("copy");
  if (copy_button != null) {
    copy_button.addEventListener("click", (e) => {
      let txt = get_table_text();
      navigator.clipboard.writeText(txt);
      copy_button.classList.add("secondary");
      copy_button.innerHTML = "Kopierat!";
    });
  }

  function reset_copy_button() {
    copy_button.classList.remove("secondary");
    copy_button.innerHTML = "Kopiera";
  }
  
  const all_inputs = document.querySelectorAll("#data input");
  all_inputs.forEach((el) => {
    el.addEventListener("input", (e) => {
      reset_copy_button();
    });
  });

  const toggles = document.querySelectorAll(".toggle");
  toggles.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.target.parentNode.parentNode.classList.toggle("disabled");
      reset_copy_button();
    });
  });
}

document.addEventListener("htmx:afterSettle", (e) => {
  console.log(e);
  init_results();
});
