import { CommonModule } from '@angular/common';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-team-goals',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './team-goals.component.html',
  styleUrls: ['./team-goals.component.css']
})
export class TeamGoalsComponent {

  base = 'http://localhost:8000';

  teamIdQuery: string = '';
  teamNameQuery: string = '';

  teamError: string | null = null;
  showTable = false;

  goalsData: { home_goals: number; away_goals: number } | null = null;

  constructor(private http: HttpClient) {}

  searchGoals(): void {
    this.teamError = null;
    this.showTable = false;
    this.goalsData = null;

    const id = this.teamIdQuery.trim();
    const name = this.teamNameQuery.trim();

    if (!id && !name) {
      this.teamError = 'Please enter either Team ID or Team Name.';
      return;
    }

    if (id && !/^-?\d+$/.test(id)) {
      this.teamError = 'Team ID must be an integer.';
      return;
    }

    if (id && Number(id) <= 0) {
      this.teamError = 'Team ID must be a positive integer.';
      return;
    }

    if (!id && /^\d+$/.test(name)) {
      this.teamError = 'Team Name must be a valid string.';
      return;
    }

    let params = new HttpParams();

    if (id) {
      params = params.set('team_id', id);
    } else {
      params = params.set('team_name', name);
    }

    this.http.get<any>(`${this.base}/teams/matches`, { params }).subscribe({
      next: (res) => {
        if (!res || !res.data) {
          this.teamError = 'Unexpected response from server.';
          return;
        }

        this.goalsData = res.data;
        this.showTable = true;
      },
      error: (err) => {
        this.teamError = err?.error?.detail ?? 'Error fetching Team Goals Info';
      }
    });
  }

  
  hideTable(): void {
    this.showTable = false;
  }
}
