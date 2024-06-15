const COPY_SUCCESS_INNERHTML = 'Kopierat!  <i style="color: green;" id="copy-symbol" class="fa fa-copy"></i>';
var focus_listener = false;

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
    val = c.value.trim();
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

function init_datalist(list_id, data) {
  const data_list = document.getElementById(list_id);
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
  if (dictionary.includes(el.value.trim().toLowerCase())) {
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

  const species_inputs = document.querySelectorAll("input.species");
  species_inputs.forEach((el) => {
    validate_species(el);
    el.addEventListener("input", (e) => {
      validate_species(e.target);
    });
  });
      
  const copy_button = document.getElementById("copy");
  if (copy_button != null) {
    copy_button.setAttribute("init_innerHTML", copy_button.innerHTML)
    copy_button.addEventListener("click", (e) => {
      copy_button.setAttribute("current_text", get_table_text());
      navigator.clipboard.writeText(copy_button.getAttribute("current_text"));
      copy_button.classList.add("secondary");
      copy_button.innerHTML = COPY_SUCCESS_INNERHTML;
      let goto_artportalen_step = document.querySelector("#step-go-to-artporalen");
      if(goto_artportalen_step != null) {
        goto_artportalen_step.classList.remove("hidden");
      }
    });
  }

  function reset_copy_button() {
    if(copy_button.hasAttribute("current_text") && copy_button.getAttribute("current_text") != navigator.clipboard.readText()){
      copy_button.classList.remove("secondary");
      copy_button.innerHTML = copy_button.getAttribute("init_innerHTML");
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
      document.getElementById("step-easter-egg").classList.remove("hidden");
    });
  }
}

document.addEventListener("htmx:afterSettle", (e) => {
  init_results();
});
