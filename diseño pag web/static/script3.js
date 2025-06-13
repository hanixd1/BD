// Variables para almacenar selecciones
let medicoSeleccionado = null;
let fechaSeleccionada = null;
let especialidadSeleccionada = null;

// Función para mostrar alertas
function mostrarAlerta(mensaje, tipo = 'error') {
  const alertasDiv = document.getElementById('alertas');
  alertasDiv.innerHTML = `<div class="alert ${tipo}">${mensaje}</div>`;
  setTimeout(() => {
    alertasDiv.innerHTML = '';
  }, 5000);
}

// Función para limpiar el formulario
function limpiarFormulario() {
  // Limpiar selecciones de médicos
  document.querySelectorAll('.doctor-card').forEach(card => {
    card.classList.remove('selected');
  });
  
  // Limpiar selección de fechas
  document.querySelectorAll('.calendar-days span').forEach(day => {
    day.classList.remove('selected');
  });
  
  // Limpiar selección de especialidades
  document.querySelectorAll('.specialties-list span').forEach(specialty => {
    specialty.classList.remove('selected');
  });
  
  // Mostrar todos los médicos nuevamente
  document.querySelectorAll('.doctor-card').forEach(card => {
    card.style.display = 'block';
  });
  
  // Limpiar campos del formulario
  document.getElementById('medico_seleccionado').value = '';
  document.getElementById('fecha_seleccionada').value = '';
  document.getElementById('especialidad_seleccionada').value = '';
  document.getElementById('hora').value = '';
  document.getElementById('minutos').value = '';
  
  // Limpiar variables
  medicoSeleccionado = null;
  fechaSeleccionada = null;
  especialidadSeleccionada = null;
  
  // Limpiar alertas
  document.getElementById('alertas').innerHTML = '';
  
  mostrarAlerta('Formulario limpiado correctamente', 'success');
}

// Manejo de selección de médicos
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.doctor-card').forEach(card => {
    card.addEventListener('click', function() {
      // Remover selección anterior
      document.querySelectorAll('.doctor-card').forEach(c => c.classList.remove('selected'));
      
      // Agregar selección actual
      this.classList.add('selected');
      
      // Guardar datos
      medicoSeleccionado = this.getAttribute('data-doctor');
      especialidadSeleccionada = this.getAttribute('data-especialidad');
      
      // Actualizar campos ocultos
      document.getElementById('medico_seleccionado').value = medicoSeleccionado;
      document.getElementById('especialidad_seleccionada').value = especialidadSeleccionada;
      
      // Destacar especialidad correspondiente
      document.querySelectorAll('.specialties-list span').forEach(s => s.classList.remove('selected'));
      const especialidadElement = document.querySelector(`[data-especialidad="${especialidadSeleccionada}"]`);
      if (especialidadElement) {
        especialidadElement.classList.add('selected');
      }
    });
  });

  // Manejo de selección de fecha
  document.querySelectorAll('.calendar-days span:not(.disabled)').forEach(day => {
    day.addEventListener('click', function() {
      // Remover selección anterior
      document.querySelectorAll('.calendar-days span').forEach(d => d.classList.remove('selected'));
      
      // Agregar selección actual
      this.classList.add('selected');
      
      // Guardar fecha
      fechaSeleccionada = this.getAttribute('data-date');
      document.getElementById('fecha_seleccionada').value = fechaSeleccionada;
    });
  });

  // Manejo de selección de especialidades (filtro)
  document.querySelectorAll('.specialties-list span').forEach(specialty => {
    specialty.addEventListener('click', function() {
      const especialidad = this.getAttribute('data-especialidad');
      
      // Filtrar médicos por especialidad
      document.querySelectorAll('.doctor-card').forEach(card => {
        if (card.getAttribute('data-especialidad') === especialidad) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
      
      // Destacar especialidad seleccionada
      document.querySelectorAll('.specialties-list span').forEach(s => s.classList.remove('selected'));
      this.classList.add('selected');
    });
  });

  // Validación del formulario
  document.getElementById('medicoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const medico = document.getElementById('medico_seleccionado').value;
    const fecha = document.getElementById('fecha_seleccionada').value;
    const hora = document.getElementById('hora').value;
    const minutos = document.getElementById('minutos').value;
    
    // Validaciones
    if (!medico) {
      mostrarAlerta('Por favor selecciona un médico.');
      return;
    }
    
    if (!fecha) {
      mostrarAlerta('Por favor selecciona una fecha.');
      return;
    }
    
    if (!hora || !minutos) {
      mostrarAlerta('Por favor selecciona una hora completa.');
      return;
    }
    
    // Si todo está bien, enviar el formulario
    mostrarAlerta('Cita confirmada exitosamente!', 'success');
    
    // Aquí puedes enviar el formulario o hacer una petición AJAX
    setTimeout(() => {
      this.submit();
    }, 2000);
  });
});