function Formset(element) {
  /*
    Dynamic Formset handler for Django formsets.

  Events:

    * init.formset
    * add-form.formset
    * remove-form.formset
    * renumber-form.formset

  */
  if (!(this instanceof Formset)) {
    return new Formset(element);
  }
  var formset = this;
  var emptyForm = element.querySelector('.empty-form').firstElementChild;
  var formsList = element.querySelector('.forms');

  var initialForms = element.querySelector('[name$=INITIAL_FORMS]');
  var totalForms = element.querySelector('[name$=TOTAL_FORMS]');
  var prefix = initialForms.name.replace(/INITIAL_FORMS$/, '');

  function addForm(event) {
    // Duplicate empty form.
    var newForm = emptyForm.cloneNode(true);
    // Update all references to __prefix__ in the elements names.
    renumberForm(newForm, '__prefix__', totalForms.value);
    // Make it able to delete itself.
    newForm.querySelector('[data-formset-remove-form]').addEventListener('click', removeForm);
    // Append the new form to the formsList.
    formsList.insertAdjacentElement('beforeend', newForm);
    element.dispatchEvent(new CustomEvent('add-form.formset', {
      detail: {
        form: newForm,
        formset: formset
      }
    }));
    // Update the totalForms.value
    totalForms.value = Number(totalForms.value) + 1;
  }

  function getForm(target) {
    var parent = target.parentElement;
    if (parent == document) {
      return null;
    }
    if (parent == formsList) {
      return target;
    }
    return getForm(parent);
  }

  function renumberForm(form, oldValue, newValue) {
    var matchValue = prefix + oldValue.toString()
    var match = new RegExp(matchValue);
    var replace = prefix + newValue.toString();

    ['name', 'id', 'for'].forEach(function (attr) {
      form.querySelectorAll('[' + attr + '*=' + matchValue + ']').forEach(function (el) {
        el.setAttribute(attr, el.getAttribute(attr).replace(match, replace));
      });
    });

    element.dispatchEvent(new CustomEvent('renumber-form.formset', {
      detail: {
        form: form,
        oldValue: oldValue,
        newValue: newValue,
        formset: formset
      }
    }));
  }

  function removeForm(event) {
    // Find the form "row": the child of formsList that is the parent of the element
    // that triggered this event.
    var formToRemove = getForm(event.target);
    // Renumber the rows that come after us.
    var nextElement = formToRemove.nextElementSibling;
    var nextElementIndex = Array.prototype.indexOf.call(formsList.children, formToRemove);
    while (nextElement) {
      renumberForm(nextElement, nextElementIndex + 1, nextElementIndex);
      nextElement = nextElement.nextElementSibling;
      nextElementIndex = nextElementIndex + 1;
    }
    // Remove this row.
    formToRemove.remove();
    element.dispatchEvent(new CustomEvent('remove-form.formset', {
      detail: {
        form: formToRemove,
        formset: formset
      }
    }));
    // Decrement the management form's count.
    totalForms.value = Number(totalForms.value) - 1;
  }

  element.querySelector('[data-formset-add-form]').addEventListener('click', addForm);
  element.formset = this;

  element.dispatchEvent(new CustomEvent('init.formset', {
    detail: {
      formset: this
    }
  }));

  this.addForm = addForm;
}

new Formset(document.querySelector('#form1'));
