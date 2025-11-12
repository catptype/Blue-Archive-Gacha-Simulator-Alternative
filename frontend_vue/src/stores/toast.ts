import { ref } from 'vue';
import { defineStore } from 'pinia';

// Interface for a toast object, adding a unique ID
export interface Toast {
  id: number;
  achievement_name: string;
  image_url: string;
  // Add any other achievement properties you want to display
}

export const useToastStore = defineStore('toasts', () => {
  const toasts = ref<Toast[]>([]);
  let idCounter = 0;

  /**
   * Adds a new toast notification to the list.
   * @param achievement The achievement data from the API.
   */
  function addToast(achievement: any) {
    const id = idCounter++;
    toasts.value.push({
      id,
      achievement_name: achievement.achievement_name,
      image_url: achievement.image_url,
    });

    // Automatically remove the toast after 7 seconds
    setTimeout(() => {
      removeToast(id);
    }, 7000);
  }

  /**
   * Removes a toast from the list by its unique ID.
   * @param id The ID of the toast to remove.
   */
  function removeToast(id: number) {
    const index = toasts.value.findIndex(t => t.id === id);
    if (index > -1) {
      toasts.value.splice(index, 1);
    }
  }

  return { toasts, addToast, removeToast };
});