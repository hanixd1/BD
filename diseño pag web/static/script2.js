// Variables globales para el calendario
let currentDate = new Date();
let selectedDate = null;

const monthNames = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];

// Función para generar el calendario
function generateCalendar() {
  const grid = document.getElementById('calendarGrid');
  const monthYear = document.getElementById('monthYear');
  
  // Limpiar calendario existente
  grid.innerHTML = '';
  
  // Agregar encabezados de días
  const dayHeaders = ['D', 'L', 'M', 'M', 'J', 'V', 'S'];
  dayHeaders.forEach(day => {
    const header = document.createElement('div');
    header.className = 'calendar-day-header';
    header.textContent = day;
    grid.appendChild(header);
  });
  
  // Actualizar display de mes/año
  monthYear.textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
  
  // Obtener primer día del mes y número de días
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const daysInMonth = lastDay.getDate();
  const startingDayOfWeek = firstDay.getDay();
  
  // Agregar celdas vacías para días antes del inicio del mes
  for (let i = 0; i < startingDayOfWeek; i++) {
    const emptyDay = document.createElement('div');
    emptyDay.className = 'calendar-day other-month';
    grid.appendChild(emptyDay);
  }
  
  // Agregar días del mes
  const today = new Date();
  for (let day = 1; day <= daysInMonth; day++) {
    const dayElement = document.createElement('div');
    dayElement.className = 'calendar-day';
    dayElement.textContent = day;
    
    // Verificar si es hoy
    if (year === today.getFullYear() && 
        month === today.getMonth() && 
        day === today.getDate()) {
      dayElement.classList.add('today');
    }
    
    // Verificar si está seleccionado
    if (selectedDate && 
        year === selectedDate.getFullYear() && 
        month === selectedDate.getMonth() && 
        day === selectedDate.getDate()) {
      dayElement.classList.add('selected');
    }
    
    // Agregar evento click
    dayElement.addEventListener('click', () => selectDate(year, month, day));
    grid.appendChild(dayElement);
  }
}

// Función para seleccionar una fecha
function selectDate(year, month, day) {
  // Remover selección anterior
  document.querySelectorAll('.calendar-day.selected').forEach(el => {
    el.classList.remove('selected');
  });
  
  // Agregar selección al día clickeado
  event.target.classList.add('selected');
  selectedDate = new Date(year, month, day);
}

// Función para cambiar mes
function changeMonth(direction) {
  currentDate.setMonth(currentDate.getMonth() + direction);
  generateCalendar();
}

// Funcionalidad de botones de opciones
function initializeOptionButtons() {
  document.querySelectorAll('.option-buttons').forEach(group => {
    group.addEventListener('click', (e) => {
      if (e.target.classList.contains('option-btn')) {
        // Remover selección de hermanos
        group.querySelectorAll('.option-btn').forEach(btn => {
          btn.classList.remove('selected');
        });
        // Agregar selección al botón clickeado
        e.target.classList.add('selected');
      }
    });
  });
}

// Funcionalidad del toggle switch
function initializeToggleSwitch() {
  document.getElementById('visitToggle').addEventListener('click', function() {
    this.classList.toggle('active');
    const status = document.getElementById('visitStatus');
    if (this.classList.contains('active')) {
      status.textContent = 'TIENE VISITA PREVIA';
    } else {
      status.textContent = 'NO TIENE VISITA PREVIA';
    }
  });
}

// Funcionalidad del checkbox
function initializeCheckbox() {
  document.getElementById('confirmCheckbox').addEventListener('click', function() {
    this.classList.toggle('checked');
  });
}

// Función para crear y enviar el formulario al backend
function enviarDatosAlBackend() {
  const condicion = document.getElementById('condicionMedica').value;
  const descripcion = document.getElementById('descripcion').value;
  const confirmado = document.getElementById('confirmCheckbox').classList.contains('checked');
  
  // Validar campos requeridos
  if (!condicion || !descripcion) {
    alert('Por favor complete los campos de condición médica y descripción');
    return false;
  }
  
  if (!confirmado) {
    alert('Por favor confirme que ha revisado los datos de su cita');
    return false;
  }
  
  // Recopilar datos seleccionados
  const selectedOptions = {};
  document.querySelectorAll('.option-buttons').forEach(group => {
    const groupName = group.getAttribute('data-group');
    const selectedBtn = group.querySelector('.option-btn.selected');
    if (selectedBtn) {
      selectedOptions[groupName] = selectedBtn.getAttribute('data-value');
    }
  });
  
  // Crear formulario dinámico
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/procesar_descripcion';
  
  // Agregar campos al formulario
  const campos = {
    'condicionMedica': condicion,
    'descripcion': descripcion,
    'gravedad': selectedOptions.gravedad || '',
    'molestia': selectedOptions.molestia || '',
    'persistencia': selectedOptions.persistencia || '',
    'fechaVisita': selectedDate ? selectedDate.toISOString().split('T')[0] : '',
    'tieneVisitaPrevia': document.getElementById('visitToggle').classList.contains('active')
  };
  
  Object.keys(campos).forEach(key => {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = campos[key];
    form.appendChild(input);
  });
  
  // Agregar formulario al body y enviarlo
  document.body.appendChild(form);
  form.submit();
  
  return true;
}

// Funciones de los botones principales
function continuar() {
  enviarDatosAlBackend();
}

function limpiarFormulario() {
  if (confirm('¿Está seguro que desea limpiar todos los campos?')) {
    // Limpiar campos de texto
    document.getElementById('condicionMedica').value = '';
    document.getElementById('descripcion').value = '';
    
    // Limpiar selecciones de opciones
    document.querySelectorAll('.option-btn.selected').forEach(btn => {
      btn.classList.remove('selected');
    });
    
    // Limpiar checkbox
    document.getElementById('confirmCheckbox').classList.remove('checked');
    
    // Limpiar fecha seleccionada
    selectedDate = null;
    generateCalendar();
    
    // Resetear toggle switch
    const toggle = document.getElementById('visitToggle');
    toggle.classList.remove('active');
    document.getElementById('visitStatus').textContent = 'NO TIENE VISITA PREVIA';
  }
}

function retroceder() {
  if (confirm('¿Está seguro que desea retroceder? Se perderán los datos ingresados.')) {
    window.location.href = '/retroceder_a_pagina1';
  }
}

function goToPage1() {
  if (confirm('¿Está seguro que desea ir a la página anterior? Se perderán los datos ingresados.')) {
    window.location.href = '/';
  }
}

// Función para obtener datos del formulario (útil para debugging)
function getFormData() {
  const selectedOptions = {};
  document.querySelectorAll('.option-buttons').forEach(group => {
    const groupName = group.getAttribute('data-group');
    const selectedBtn = group.querySelector('.option-btn.selected');
    if (selectedBtn) {
      selectedOptions[groupName] = selectedBtn.getAttribute('data-value');
    }
  });
  
  return {
    condicionMedica: document.getElementById('condicionMedica').value,
    descripcion: document.getElementById('descripcion').value,
    opciones: selectedOptions,
    fechaSeleccionada: selectedDate,
    tieneVisitaPrevia: document.getElementById('visitToggle').classList.contains('active'),
    confirmado: document.getElementById('confirmCheckbox').classList.contains('checked')
  };
}

// Inicializar todo cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
  generateCalendar();
  initializeOptionButtons();
  initializeToggleSwitch();
  initializeCheckbox();
  
  console.log('Sistema de gestión médica inicializado correctamente');
});