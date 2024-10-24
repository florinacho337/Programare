export interface TaskProps {
  id?: string;
  name: string;
  description?: string;
  deadline: Date;
  finished?: boolean;
  progress: number;
  important: boolean;
  urgent: boolean;
}
