// Chatbot functionality with localStorage persistence
class Chatbot {
  constructor() {
    this.messages = this.loadMessages();
    this.isOpen = false;
    this.init();
  }

  init() {
    this.renderMessages();
    this.attachEventListeners();
  }

  loadMessages() {
    const stored = localStorage.getItem('chatbot_messages');
    if (stored) {
      return JSON.parse(stored);
    }
    // Default welcome message
    return [
      {
        type: 'bot',
        text: '¡Hola! Soy el asistente virtual de Wawalu. ¿En qué puedo ayudarte hoy?',
        timestamp: new Date().toISOString()
      }
    ];
  }

  saveMessages() {
    localStorage.setItem('chatbot_messages', JSON.stringify(this.messages));
  }

  attachEventListeners() {
    const chatbotBtn = document.getElementById('chatbot-button');
    const closeBtn = document.getElementById('chatbot-close');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');

    chatbotBtn.addEventListener('click', () => this.toggleChat());
    closeBtn.addEventListener('click', () => this.toggleChat());

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const message = input.value.trim();
      if (message) {
        this.sendMessage(message);
        input.value = '';
      }
    });
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
    const window = document.getElementById('chatbot-window');
    window.classList.toggle('active');
    
    if (this.isOpen) {
      document.getElementById('chatbot-input').focus();
      this.scrollToBottom();
    }
  }

  sendMessage(text) {
    // Add user message
    const userMessage = {
      type: 'user',
      text: text,
      timestamp: new Date().toISOString()
    };
    this.messages.push(userMessage);
    this.saveMessages();
    this.renderMessages();
    this.scrollToBottom();

    // Show typing indicator
    this.showTypingIndicator();

    // Simulate bot response after delay
    setTimeout(() => {
      this.hideTypingIndicator();
      const botResponse = this.generateResponse(text);
      const botMessage = {
        type: 'bot',
        text: botResponse,
        timestamp: new Date().toISOString()
      };
      this.messages.push(botMessage);
      this.saveMessages();
      this.renderMessages();
      this.scrollToBottom();
    }, 1000 + Math.random() * 1000);
  }

  generateResponse(userMessage) {
    const msg = userMessage.toLowerCase();
    
    // Simple keyword-based responses
    if (msg.includes('hola') || msg.includes('buenos') || msg.includes('buenas')) {
      return '¡Hola! ¿En qué puedo ayudarte hoy?';
    }
    
    if (msg.includes('horario') || msg.includes('hora')) {
      return 'Nuestro horario de atención es de Lunes a Viernes de 8:00 AM a 5:00 PM.';
    }
    
    if (msg.includes('precio') || msg.includes('costo') || msg.includes('cuanto')) {
      return 'Los precios varían según el programa. Te invito a visitar nuestra sección de Programas o contactarnos directamente para más información.';
    }
    
    if (msg.includes('programa') || msg.includes('curso')) {
      return 'Ofrecemos programas para bebés, inicial y preescolar basados en la metodología Reggio Emilia. ¿Te gustaría conocer más sobre alguno en específico?';
    }
    
    if (msg.includes('admision') || msg.includes('inscri') || msg.includes('matricula')) {
      return 'Puedes solicitar admisión completando nuestro formulario en la sección de Admisión. ¿Necesitas ayuda con el proceso?';
    }
    
    if (msg.includes('contacto') || msg.includes('telefono') || msg.includes('correo')) {
      return 'Puedes contactarnos al +51 942 139 788 o escribirnos a diego.centeno@vallegrande.edu.pe. También estamos disponibles por WhatsApp.';
    }
    
    if (msg.includes('ubicacion') || msg.includes('direccion') || msg.includes('donde')) {
      return 'Nos encontramos en Av. Mariscal Benavides 1365, Cañete, Lima, Perú.';
    }
    
    if (msg.includes('tienda') || msg.includes('uniforme') || msg.includes('utiles')) {
      return 'Tenemos una tienda con uniformes, útiles y materiales educativos. Puedes acceder desde el menú principal.';
    }
    
    if (msg.includes('gracias')) {
      return '¡De nada! Estoy aquí para ayudarte. ¿Hay algo más en lo que pueda asistirte?';
    }
    
    if (msg.includes('adios') || msg.includes('chao')) {
      return '¡Hasta pronto! No dudes en escribirme si necesitas algo más.';
    }
    
    // Default response
    return 'Gracias por tu mensaje. Para información más específica, te recomiendo contactarnos directamente al +51 942 139 788 o visitar nuestra sección de Contacto.';
  }

  showTypingIndicator() {
    const messagesContainer = document.getElementById('chatbot-messages');
    const indicator = document.createElement('div');
    indicator.id = 'typing-indicator';
    indicator.className = 'message bot typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    messagesContainer.appendChild(indicator);
    this.scrollToBottom();
  }

  hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
      indicator.remove();
    }
  }

  renderMessages() {
    const messagesContainer = document.getElementById('chatbot-messages');
    messagesContainer.innerHTML = '';
    
    this.messages.forEach(msg => {
      const messageEl = document.createElement('div');
      messageEl.className = `message ${msg.type}`;
      messageEl.textContent = msg.text;
      messagesContainer.appendChild(messageEl);
    });
  }

  scrollToBottom() {
    const messagesContainer = document.getElementById('chatbot-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new Chatbot();
});
