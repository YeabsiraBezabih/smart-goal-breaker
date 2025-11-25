export interface Task {
  id: number;
  task_text: string;
  order: number;
  created_at: string;
}

export interface Goal {
  id: number;
  goal_text: string;
  complexity_score: number;
  created_at: string;
  tasks: Task[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function createGoal(goalText: string): Promise<Goal> {
  const response = await fetch(`${API_URL}/goals`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',  // Include cookies for session
    body: JSON.stringify({ goal_text: goalText }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create goal');
  }

  return response.json();
}

export async function getGoals(): Promise<Goal[]> {
  const response = await fetch(`${API_URL}/goals`, {
    credentials: 'include',  // Include cookies for session
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch goals');
  }

  return response.json();
}

export async function deleteGoal(goalId: number): Promise<void> {
  const response = await fetch(`${API_URL}/goals/${goalId}`, {
    method: 'DELETE',
    credentials: 'include',  // Include cookies for session
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete goal');
  }
}
