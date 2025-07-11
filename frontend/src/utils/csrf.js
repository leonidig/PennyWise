export function getCSRFToken() {
  const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='))
  return cookie ? cookie.split('=')[1] : ''
}