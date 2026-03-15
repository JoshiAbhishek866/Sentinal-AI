import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref([])
  const unreadCount = ref(0)
  const isLoading = ref(false)

  // Fetch all notifications
  async function fetchNotifications() {
    isLoading.value = true
    try {
      const token = localStorage.getItem('adminToken')
      const response = await axios.get(`${API_BASE}/admin/notifications`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      notifications.value = response.data.notifications || []
      updateUnreadCount()
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
    } finally {
      isLoading.value = false
    }
  }

  // Mark notification as read
  async function markAsRead(notificationId) {
    try {
      const token = localStorage.getItem('adminToken')
      await axios.patch(`${API_BASE}/admin/notifications/${notificationId}/read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      const notification = notifications.value.find(n => n._id === notificationId)
      if (notification) {
        notification.read = true
        updateUnreadCount()
      }
    } catch (error) {
      console.error('Failed to mark notification as read:', error)
    }
  }

  // Mark all as read
  async function markAllAsRead() {
    try {
      const token = localStorage.getItem('adminToken')
      await axios.patch(`${API_BASE}/admin/notifications/read-all`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      notifications.value.forEach(n => n.read = true)
      updateUnreadCount()
    } catch (error) {
      console.error('Failed to mark all as read:', error)
    }
  }

  // Delete notification
  async function deleteNotification(notificationId) {
    try {
      const token = localStorage.getItem('adminToken')
      await axios.delete(`${API_BASE}/admin/notifications/${notificationId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      notifications.value = notifications.value.filter(n => n._id !== notificationId)
      updateUnreadCount()
    } catch (error) {
      console.error('Failed to delete notification:', error)
    }
  }

  // Update unread count
  function updateUnreadCount() {
    unreadCount.value = notifications.value.filter(n => !n.read).length
  }

  // Get unread notifications
  const unreadNotifications = computed(() => {
    return notifications.value.filter(n => !n.read)
  })

  // Get recent notifications (last 5)
  const recentNotifications = computed(() => {
    return notifications.value.slice(0, 5)
  })

  return {
    notifications,
    unreadCount,
    isLoading,
    unreadNotifications,
    recentNotifications,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification
  }
})
