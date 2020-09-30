elements.forEach((element) => {
    var input = element.querySelector('.ui-widget-content .ui-autocomplete-input')
    input.value = 'newsletter'
    var button = element.querySelector('input.button')
    button.click()
})
