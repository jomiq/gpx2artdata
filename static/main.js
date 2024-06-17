COPY_SUCCESS_INNERHTML =
  '<span class="rows-selected"></span> kopierade!  <i class="fa fa-copy">';

function get_table_heading_text(el) {
  const cells = document.querySelectorAll("#data thead tr th:not(.control)");
  var res = [];
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
  var res = [];
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
  var res = [get_table_heading_text()];

  var rows = get_table_rows();
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
    console.log(document.querySelector(".error"));
    return;
  }

  const row_count = document.getElementById("row-count");
  const species_inputs = document.querySelectorAll("input.species");
  const copy_button = document.getElementById("copy");
  const all_inputs = document.querySelectorAll("#data input");
  const toggles = document.querySelectorAll(".toggle");
  const goto_artportalen_step = document.querySelector(
    "#step-go-to-artporalen"
  );
  const ap_link = document.getElementById("ap-link");

  var rows_selected = row_count.getAttribute("total_rows");
  update_rows_selected();
  function update_rows_selected() {
    elements = document.querySelectorAll(".rows-selected");
    elements.forEach((el) => {
      el.innerHTML = `${rows_selected} observation${
        rows_selected != 1 ? "er" : ""
      }`;
    });
  }

  species_inputs.forEach((el) => {
    validate_species(el);
    el.addEventListener("input", (e) => {
      validate_species(e.target);
    });
  });

  copy_button.setAttribute("init_innerHTML", copy_button.innerHTML);
  copy_button.addEventListener("click", (e) => {
    var t = get_table_text()
    copy_button.setAttribute("copied", true);
    navigator.clipboard.writeText(t);
    copy_button.classList.add("secondary");
    copy_button.innerHTML = COPY_SUCCESS_INNERHTML;
    update_rows_selected();
    goto_artportalen_step.classList.remove("not-yet");
  });

  function reset_copy_button() {
    if (copy_button.hasAttribute("copied")) {
      copy_button.setAttribute("copied", false);
      copy_button.classList.remove("secondary");
      copy_button.innerHTML = copy_button.getAttribute("init_innerHTML");
      goto_artportalen_step.classList.add("not-yet");
      update_rows_selected();
    }
  }

  all_inputs.forEach((el) => {
    el.addEventListener("input", (e) => {
      reset_copy_button();
    });
  });

  toggles.forEach((button) => {
    button.addEventListener("change", (e) => {
      var el = e.target;

      if (el.checked) {
        el.parentNode.parentNode.classList.remove("disabled");
        rows_selected++;
      } else {
        el.parentNode.parentNode.classList.add("disabled");
        rows_selected--;
      }
      update_rows_selected();
    });
  });

  if (ap_link != null) {
    ap_link.addEventListener("click", (e) => {
      document.getElementById("step-easter-egg").classList.remove("hidden");
    });
  }
}

document.addEventListener("htmx:afterSettle", (e) => {
  init_results();
});
