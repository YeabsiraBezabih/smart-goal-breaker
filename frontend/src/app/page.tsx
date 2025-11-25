"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { createGoal, getGoals, deleteGoal, Goal } from "@/lib/api";
import { GoalDisplay } from "@/components/GoalDisplay";
import { Sparkles, ArrowRight, Target } from "lucide-react";

export default function Home() {
  const [goalInput, setGoalInput] = useState("");
  const [goals, setGoals] = useState<Goal[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadGoals();
  }, []);

  async function loadGoals() {
    try {
      const data = await getGoals();
      setGoals(data);
    } catch (err) {
      console.error("Failed to load goals:", err);
      // Don't show error for initial load, just empty state
    } finally {
      setIsFetching(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!goalInput.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const newGoal = await createGoal(goalInput);
      setGoals([newGoal, ...goals]);
      setGoalInput("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleDelete(goalId: number) {
    try {
      await deleteGoal(goalId);
      setGoals(goals.filter(g => g.id !== goalId));
    } catch (err) {
      throw err;  // Re-throw to let GoalDisplay handle the error
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-muted/20 p-4 md:p-8 lg:p-12">
      <div className="max-w-3xl mx-auto space-y-8">

        {/* Header */}
        <div className="text-center space-y-4 py-8">
          <div className="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-4">
            <Target className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight lg:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-primary to-purple-600">
            Smart Goal Breaker
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Turn your vague ambitions into actionable steps with AI.
          </p>
        </div>

        {/* Input Section */}
        <Card className="border-2 shadow-lg">
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4">
              <Input
                placeholder="e.g., 'Launch a startup' or 'Learn Python'"
                value={goalInput}
                onChange={(e) => setGoalInput(e.target.value)}
                className="flex-1 text-lg py-6"
                disabled={isLoading}
              />
              <Button
                type="submit"
                size="lg"
                disabled={isLoading || !goalInput.trim()}
                className="md:w-32 font-bold transition-all hover:scale-105"
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <span className="animate-spin">✨</span>
                    Processing
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    Break It
                    <Sparkles className="w-4 h-4" />
                  </div>
                )}
              </Button>
            </form>
            {error && (
              <p className="text-destructive mt-3 text-sm font-medium animate-in fade-in slide-in-from-top-1">
                Error: {error}
              </p>
            )}
          </CardContent>
        </Card>

        {/* Results Section */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold tracking-tight">Your Goals</h2>
            <span className="text-sm text-muted-foreground">{goals.length} goals tracked</span>
          </div>

          {isLoading && (
            <Card className="w-full mb-6 border-primary/20 border-dashed">
              <CardContent className="pt-6 space-y-4">
                <div className="flex justify-between items-center">
                  <Skeleton className="h-8 w-1/3" />
                  <Skeleton className="h-6 w-20" />
                </div>
                <div className="space-y-3 pt-4">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <div key={i} className="flex gap-4">
                      <Skeleton className="h-8 w-8 rounded-full shrink-0" />
                      <Skeleton className="h-6 w-full" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {isFetching ? (
            <div className="space-y-4">
              {[1, 2].map((i) => (
                <Skeleton key={i} className="h-64 w-full rounded-xl" />
              ))}
            </div>
          ) : goals.length > 0 ? (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
              {goals.map((goal) => (
                <GoalDisplay key={goal.id} goal={goal} onDelete={handleDelete} />
              ))}
            </div>
          ) : (
            !isLoading && (
              <div className="text-center py-12 text-muted-foreground bg-muted/10 rounded-xl border border-dashed">
                <Sparkles className="w-12 h-12 mx-auto mb-4 opacity-20" />
                <p className="text-lg font-medium">No goals yet</p>
                <p>Type a goal above to get started!</p>
              </div>
            )
          )}
        </div>
      </div>
    </main>
  );
}
