$(document).ready(function() {
  $('select').selectize({
    sortField: 'text'
  });
});

let options

function populateOptions(id, optionsArr) {
  console.log(`populating ${id} with ${optionsArr}`)
  const select = document.getElementById(id)
  //select.selectize.clear();
  select.selectize.clearOptions();
  for (const option of optionsArr) {
    select.selectize.addOption({
      value: option,
      text: option
    });
  }
  select.selectize.refreshOptions(false)
}

async function onload(){
  const response = await fetch("/options")
  if (!response.ok) {
    throw new Error(`Request Failed!!!: ${response.status}`)
  }
  options = await response.json()
  make = Object.keys(options[0])
  console.log(`MAKE: ${make}`)
  populateOptions("make-select", make);
  populateOptions("body-select", options[2]);
  populateOptions("drivetrain-select", options[1]);
  populateOptions("transmission-select", options[3]);
  populateOptions("fuel-select", options[4]);
}

function updateModels(){
  user_make = document.getElementById("make-select").value
  populateOptions("model-select", options[0][user_make])
}