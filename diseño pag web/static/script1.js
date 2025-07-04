// Referencias a elementos del DOM
const form = document.getElementById('citaForm');
const confirmarCheckbox = document.getElementById('confirmar');
const btnContinuar = document.getElementById('btnContinuar');
const btnLimpiar = document.getElementById('btnLimpiar');
const btnCancelar = document.getElementById('btnCancelar');

// Funcionalidad para botones del menú principal
document.addEventListener('DOMContentLoaded', function() {
  // Obtener todos los botones del menú principal
  const mainNavButtons = document.querySelectorAll('.main-nav .nav-button');
  
  mainNavButtons.forEach(function(button, index) {
    button.addEventListener('click', function() {
      // El primer botón es "GESTIÓN DE CITAS MÉDICAS" (índice 0)
      if (index === 0) {
        // Permitir acceso a Gestión de Citas Médicas
        console.log('Acceso permitido a Gestión de Citas Médicas');
        // Aquí puedes agregar la lógica para mostrar/ocultar secciones
        // Por ejemplo: mostrar la sección actual
      } else {
        // Bloquear acceso a las demás secciones
        alert('Acceso bloqueado');
        console.log('Acceso bloqueado a: ' + button.textContent);
      }
    });
  });

  // Funcionalidad para botones del menú secundario
  const secondaryNavButtons = document.querySelectorAll('.top-nav button');
  
  secondaryNavButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      const buttonText = button.textContent.trim();
      
      if (buttonText === 'AGENDAR CITA') {
        // Permitir acceso a Agendar Cita (funcionalidad actual)
        console.log('Acceso permitido a Agendar Cita');
        // La funcionalidad actual ya está implementada
      } else if (buttonText === 'INGRESAR DESCRIPCIÓN DE LA CONDICIÓN MÉDICA') {
        // Bloquear acceso
        alert('Acceso bloqueado');
        console.log('Acceso bloqueado a: Descripción de Condición Médica');
      } else if (buttonText === 'SELECCIONAR MÉDICO') {
        // Bloquear acceso
        alert('Acceso bloqueado');
        console.log('Acceso bloqueado a: Seleccionar Médico');
      }
    });
  });
});

// Habilitar/deshabilitar botón continuar según checkbox
confirmarCheckbox.addEventListener('change', function() {
  btnContinuar.disabled = !this.checked;
});

// Función para limpiar el formulario
btnLimpiar.addEventListener('click', function() {
  if (confirm('¿Está seguro que desea limpiar todos los campos?')) {
    // Limpiar todos los inputs de texto y número
    document.getElementById('paciente').value = '';
    document.getElementById('codigo').value = '';
    document.getElementById('telefono').value = '+51';
    document.getElementById('direccion').value = 'S/N';
    document.getElementById('tutor').value = 'Ninguno';
    document.getElementById('motivo').value = '';
    document.getElementById('edad').value = '';
    
    // Limpiar selects
    document.getElementById('sexo').selectedIndex = 0;
    document.getElementById('seguro').selectedIndex = 0;
    
    // Limpiar radio buttons de modalidad
    const modalidadRadios = document.querySelectorAll('input[name="modalidad"]');
    modalidadRadios.forEach(radio => {
      radio.checked = false;
    });
    
    // Limpiar fecha
    document.getElementById('fecha').value = '';
    
    // Desmarcar checkbox de confirmación
    confirmarCheckbox.checked = false;
    btnContinuar.disabled = true;
    
    // Quitar cualquier borde rojo de validación
    const allFields = form.querySelectorAll('input, select, textarea');
    allFields.forEach(field => {
      field.style.borderColor = '';
    });
    
    console.log('Formulario limpiado correctamente');
  }
});

// Función para cancelar
btnCancelar.addEventListener('click', function() {
  if (confirm('¿Está seguro que desea cancelar? Se perderán todos los datos ingresados.')) {
    window.location.href = "/cancelar";
  }
});

// Función para continuar - VERSIÓN FLASK
btnContinuar.addEventListener('click', function(e) {
  e.preventDefault(); // Prevenir comportamiento por defecto
  
  // Validar que todos los campos requeridos estén llenos
  const requiredFields = form.querySelectorAll('[required]');
  let allValid = true;
  
  requiredFields.forEach(field => {
    if (!field.value.trim() && field.type !== 'radio') {
      allValid = false;
      field.style.borderColor = 'red';
    } else {
      field.style.borderColor = '';
    }
  });

  // Validar radio buttons de modalidad
  const modalidadRadios = form.querySelectorAll('input[name="modalidad"]');
  const modalidadSelected = Array.from(modalidadRadios).some(radio => radio.checked);
  if (!modalidadSelected) {
    allValid = false;
    alert('Por favor seleccione una modalidad de atención.');
    return;
  }

  if (allValid) {
    // Enviar el formulario al servidor Flask
    form.submit();
  } else {
    alert('Por favor complete todos los campos requeridos.');
  }
});

// Validación en tiempo real para quitar el borde rojo cuando se corrija
const allInputs = form.querySelectorAll('input, select, textarea');
allInputs.forEach(input => {
  input.addEventListener('input', function() {
    if (this.style.borderColor === 'red' && this.value.trim()) {
      this.style.borderColor = '';
    }
  });
});

// Función adicional para mostrar efectos visuales en botones bloqueados (opcional)
function addBlockedButtonStyles() {
  const style = document.createElement('style');
  style.textContent = `
    .nav-button.blocked:hover {
      background-color: #dc3545 !important;
      cursor: not-allowed;
    }
    
    .top-nav button.blocked:hover {
      background-color: #dc3545 !important;
      cursor: not-allowed;
    }
  `;
  document.head.appendChild(style);
}

// Aplicar estilos de botones bloqueados al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  addBlockedButtonStyles();
  
  // Marcar botones bloqueados (opcional - para efectos visuales)
  const mainNavButtons = document.querySelectorAll('.main-nav .nav-button');
  mainNavButtons.forEach(function(button, index) {
    if (index !== 0) { // Todos excepto "GESTIÓN DE CITAS MÉDICAS"
      button.classList.add('blocked');
    }
  });
  
  const secondaryNavButtons = document.querySelectorAll('.top-nav button');
  secondaryNavButtons.forEach(function(button) {
    const buttonText = button.textContent.trim();
    if (buttonText !== 'AGENDAR CITA') {
      button.classList.add('blocked');
    }
  });
});