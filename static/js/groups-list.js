var isRotated = false;

function rotate(event) {

  if (!isRotated) {
    document.getElementById('down-icon').classList.add('rotated');
    document.getElementById('header-popover').classList.add('popover-opened');
    event.stopPropagation();

    document.addEventListener('click', function ($event) {

      let isClickedOutside = true;
      let isClickedPersonInfoWrapper = false;

      for (const path of $event.composedPath()) {
        if (path.id === 'header-popover') {
          isClickedOutside = false;
        }
        if (path.id === 'person-info-wrapper-id') {
          isClickedPersonInfoWrapper = true;
        }
      }

      if (isClickedOutside) {
        document.removeEventListener('click', arguments.callee, false);

        if (!isClickedPersonInfoWrapper) {
          document.getElementById('person-info-wrapper-id').click();
        }
      }

    });
  } else {
    document.getElementById('down-icon').classList.remove('rotated');
    document.getElementById('header-popover').classList.remove('popover-opened');
  }

  isRotated = !isRotated;

}

