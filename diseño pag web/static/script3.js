// Variables para almacenar selecciones
let medicoSeleccionado = null;
let fechaSeleccionada = null;
let especialidadSeleccionada = null;

// Fechas disponibles por médico (simulando base de datos)
const fechasDisponibles = {
  'carlos_marrique': ['2025-08-01', '2025-08-03', '2025-08-05', '2025-08-07', '2025-08-09', '2025-08-11', '2025-08-13'],
  'estefanie_gomez': ['2025-08-02', '2025-08-04', '2025-08-06', '2025-08-08', '2025-08-10', '2025-08-12', '2025-08-14'],
  'manolo_tiza': ['2025-08-01', '2025-08-04', '2025-08-07', '2025-08-10', '2025-08-13', '2025-08-16', '2025-08-19'],
  'ruben_alcantara': ['2025-08-03', '2025-08-05', '2025-08-07', '2025-08-09', '2025-08-11', '2025-08-15', '2025-08-17'],
  'brayan_smit': ['2025-08-02', '2025-08-06', '2025-08-09', '2025-08-12', '2025-08-15', '2025-08-18', '2025-08-21'],
  'piero_enrique': ['2025-08-01', '2025-08-05', '2025-08-08', '2025-08-11', '2025-08-14', '2025-08-17', '2025-08-20'],
  'cristhian_cardenaz': ['2025-08-03', '2025-08-06', '2025-08-10', '2025-08-13', '2025-08-16', '2025-08-19', '2025-08-22'],
  'renzo_flores': ['2025-08-02', '2025-08-07', '2025-08-12', '2025-08-14', '2025-08-16', '2025-08-18', '2025-08-21'],
  'matias_sanchez': ['2025-08-01', '2025-08-08', '2025-08-15', '2025-08-17', '2025-08-19', '2025-08-22', '2025-08-24'],
  'david_gongora': ['2025-08-04', '2025-08-09', '2025-08-11', '2025-08-16', '2025-08-18', '2025-08-20', '2025-08-23'],
  'malena_garcia': ['2025-08-02', '2025-08-05', '2025-08-09', '2025-08-12', '2025-08-16', '2025-08-19', '2025-08-23']
};

// Función para mostrar alertas
function mostrarAlerta(mensaje, tipo = 'error') {
  const alertasDiv = document.getElementById('alertas');
  alertasDiv.innerHTML = `<div class="alert ${tipo}">${mensaje}</div>`;
  setTimeout(() => {
    alertasDiv.innerHTML = '';
  }, 5000);
}

// Función para generar el calendario
function generarCalendario(fechasPermitidas = []) {
  const calendarDays = document.getElementById('calendar-days');
  calendarDays.innerHTML = '';
  
  // Días del mes de agosto 2025
  const diasPrevios = ['27', '28', '29', '30', '31'];
  const diasDelMes = Array.from({length: 31}, (_, i) => i + 1);
  
  // Agregar días del mes anterior (deshabilitados)
  diasPrevios.forEach(dia => {
    const span = document.createElement('span');
    span.textContent = dia;
    span.classList.add('disabled');
    calendarDays.appendChild(span);
  });
  
  // Agregar días del mes actual
  diasDelMes.forEach(dia => {
    const span = document.createElement('span');
    span.textContent = dia;
    
    const fechaString = `2025-08-${dia.toString().padStart(2, '0')}`;
    span.setAttribute('data-date', fechaString);
    
    // Si hay fechas permitidas y esta fecha no está en la lista, deshabilitar
    if (fechasPermitidas.length > 0 && !fechasPermitidas.includes(fechaString)) {
      span.classList.add('disabled');
    } else if (fechasPermitidas.length === 0) {
      // Si no hay médico seleccionado, deshabilitar todas las fechas
      span.classList.add('disabled');
    }
    
    calendarDays.appendChild(span);
  });
  
  // Agregar event listeners a las fechas habilitadas
  calendarDays.querySelectorAll('span:not(.disabled)').forEach(day => {
    day.addEventListener('click', function() {
      // Remover selección anterior
      calendarDays.querySelectorAll('span').forEach(d => d.classList.remove('selected'));
      
      // Agregar selección actual
      this.classList.add('selected');
      
      // Guardar fecha
      fechaSeleccionada = this.getAttribute('data-date');
      document.getElementById('fecha_seleccionada').value = fechaSeleccionada;
    });
  });
}

// Función para limpiar el formulario
function limpiarFormulario() {
  // Limpiar selecciones de médicos
  document.querySelectorAll('.doctor-card').forEach(card => {
    card.classList.remove('selected');
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
  
  // Regenerar calendario vacío
  generarCalendario([]);
  
  // Limpiar alertas
  document.getElementById('alertas').innerHTML = '';
  
  mostrarAlerta('Formulario limpiado correctamente', 'success');
}

// Función para filtrar médicos por especialidad
function filtrarMedicosPorEspecialidad(especialidad) {
  document.querySelectorAll('.doctor-card').forEach(card => {
    if (especialidad === 'todas' || card.getAttribute('data-especialidad') === especialidad) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// Función para mostrar alerta de bloqueado
function mostrarAlertaBloqueado(modulo) {
  mostrarAlerta(`🔒 ACCESO BLOQUEADO: El módulo "${modulo}" requiere permisos de administrador.`, 'error');
}

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
  // Generar calendario inicial (vacío)
  generarCalendario([]);
  
  // Manejo de selección de especialidades (filtro)
  document.querySelectorAll('.specialties-list span').forEach(specialty => {
    specialty.addEventListener('click', function() {
      const especialidad = this.getAttribute('data-especialidad');
      
      // Limpiar selección anterior de especialidades
      document.querySelectorAll('.specialties-list span').forEach(s => s.classList.remove('selected'));
      this.classList.add('selected');
      
      // Filtrar médicos por especialidad
      filtrarMedicosPorEspecialidad(especialidad);
      
      // Limpiar selección de médico y fecha si existe
      document.querySelectorAll('.doctor-card').forEach(card => {
        card.classList.remove('selected');
      });
      
      // Limpiar calendario
      generarCalendario([]);
      
      // Limpiar campos del formulario
      document.getElementById('medico_seleccionado').value = '';
      document.getElementById('fecha_seleccionada').value = '';
      medicoSeleccionado = null;
      fechaSeleccionada = null;
    });
  });

  // Manejo de selección de médicos
  document.querySelectorAll('.doctor-card').forEach(card => {
    card.addEventListener('click', function() {
      // Solo permitir selección si el médico está visible
      if (this.style.display === 'none') return;
      
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
      
      // Generar calendario con fechas disponibles para este médico
      const fechasDelMedico = fechasDisponibles[medicoSeleccionado] || [];
      generarCalendario(fechasDelMedico);
      
      // Destacar especialidad correspondiente si no está seleccionada
      const especialidadElement = document.querySelector(`.specialties-list span[data-especialidad="${especialidadSeleccionada}"]`);
      if (especialidadElement && !especialidadElement.classList.contains('selected')) {
        document.querySelectorAll('.specialties-list span').forEach(s => s.classList.remove('selected'));
        especialidadElement.classList.add('selected');
      }
      
      // Limpiar fecha seleccionada anterior
      document.getElementById('fecha_seleccionada').value = '';
      fechaSeleccionada = null;
      
      mostrarAlerta(`Médico seleccionado: ${this.textContent}. Selecciona una fecha disponible.`, 'success');
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
    
    // Validar que la fecha seleccionada esté disponible para el médico
    const fechasDelMedico = fechasDisponibles[medico] || [];
    if (!fechasDelMedico.includes(fecha)) {
      mostrarAlerta('La fecha seleccionada no está disponible para este médico.');
      return;
    }
    
    // Si todo está bien, mostrar confirmación
    const nombreMedico = document.querySelector('.doctor-card.selected').textContent;
    const fechaFormateada = new Date(fecha + 'T00:00:00').toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    
    mostrarAlerta(`¡Cita confirmada exitosamente!<br>
                   Médico: ${nombreMedico}<br>
                   Fecha: ${fechaFormateada}<br>
                   Hora: ${hora}:${minutos}`, 'success');
    
    // Simular envío del formulario
    setTimeout(() => {
      // Aquí puedes descomentar la siguiente línea para enviar el formulario real
      // this.submit();
      console.log('Datos de la cita:', {
        medico: medico,
        fecha: fecha,
        hora: hora + ':' + minutos,
        especialidad: especialidadSeleccionada
      });
    }, 3000);
  });
  
  // Funcionalidad para los cuadros de gestión
  document.querySelectorAll('.box').forEach(box => {
    box.addEventListener('click', function() {
      const textoBox = this.textContent.trim().toLowerCase();
      
      // Solo permitir acceso a "GESTIÓN DE CITAS MÉDICAS"
      if (textoBox.includes('gestión de citas médicas')) {
        mostrarAlerta('Accediendo al módulo de Gestión de Citas Médicas...', 'success');
        // Aquí puedes agregar la lógica para redirigir o mostrar el módulo
      } else {
        // Para todos los demás módulos, mostrar alerta de bloqueado
        let nombreModulo = '';
        
        if (textoBox.includes('gestión de pacientes')) {
          nombreModulo = 'GESTIÓN DE PACIENTES';
        } else if (textoBox.includes('gestión médicos')) {
          nombreModulo = 'GESTIÓN MÉDICOS';
        } else if (textoBox.includes('gestión de citas programadas')) {
          nombreModulo = 'GESTIÓN DE CITAS PROGRAMADAS';
        } else if (textoBox.includes('gestión de jaime')) {
          nombreModulo = 'GESTIÓN DE IA/ML';
        } else {
          nombreModulo = this.textContent.trim();
        }
        
        mostrarAlertaBloqueado(nombreModulo);
      }
    });
  });
});