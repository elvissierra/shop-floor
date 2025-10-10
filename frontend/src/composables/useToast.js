export function useToast() {
  function push({ type = 'info', title = '', message = '', ttl = 3500 } = {}) {
    const detail = { type, title, message, ttl }
    window.dispatchEvent(new CustomEvent('shopfloor:toast', { detail }))
  }
  return { push }
}