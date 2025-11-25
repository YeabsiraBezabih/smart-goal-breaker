import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Goal } from "@/lib/api";
import { Trash2 } from "lucide-react";
import { useState } from "react";

interface GoalDisplayProps {
  goal: Goal;
  onDelete: (goalId: number) => void;
}

export function GoalDisplay({ goal, onDelete }: GoalDisplayProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this goal?")) {
      return;
    }

    setIsDeleting(true);
    try {
      await onDelete(goal.id);
    } catch (error) {
      alert("Failed to delete goal");
      setIsDeleting(false);
    }
  };

  return (
    <Card className="w-full mb-6 overflow-hidden border-t-4 border-t-primary shadow-md hover:shadow-lg transition-shadow duration-300">
      <CardHeader className="pb-2 bg-muted/20">
        <div className="flex justify-between items-start gap-4">
          <CardTitle className="text-xl font-bold text-primary flex-1">{goal.goal_text}</CardTitle>
          <div className="flex items-center gap-2 shrink-0">
            <Badge variant={goal.complexity_score > 7 ? "destructive" : goal.complexity_score > 4 ? "secondary" : "outline"}>
              Complexity: {goal.complexity_score}/10
            </Badge>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleDelete}
              disabled={isDeleting}
              className="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
        <p className="text-xs text-muted-foreground">
          Created {new Date(goal.created_at).toLocaleDateString()}
        </p>
      </CardHeader>
      <CardContent className="pt-6">
        <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider text-muted-foreground">Action Plan</h3>
        <div className="space-y-4">
          {goal.tasks.sort((a, b) => a.order - b.order).map((task) => (
            <div key={task.id} className="flex gap-4 items-start group">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-sm group-hover:bg-primary group-hover:text-primary-foreground transition-colors duration-300">
                {task.order}
              </div>
              <p className="mt-1 text-foreground/90 leading-relaxed">{task.task_text}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
