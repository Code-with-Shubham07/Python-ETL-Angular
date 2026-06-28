import { CommonModule } from "@angular/common";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Component } from "@angular/core";
import { FormsModule } from "@angular/forms";

@Component({
    selector: 'app-team-info',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './team-info.component.html',
    styleUrls: ['./team-info.component.css']
})
export class TeamInfoComponent {
    base = 'http://localhost:8000';
    teamIdQuery: string = '';
    teamNameQuery: string = '';
    teamError: string | null = null;

    showTables = false;

    teamData: any = null;
    leagueData: any[] = [];
    countryData: any[] = [];

    constructor(private http: HttpClient) {}

    searchTeam() {
        this.teamError = null;
        this.showTables = false;

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

        this.http.get<any>(`${this.base}/teams`, { params }).subscribe({
            next: (res) => {
                if (!res || !res.data) {
                    this.teamError = 'Unexpected response from server.';
                    return;
                }

                this.teamData = res.data.team || null;
                this.leagueData = res.data.leagues || [];
                this.countryData = res.data.countries || [];

                this.showTables = true;
            },
            error: (err) => {
                this.teamError = err?.error?.detail ?? 'Error fetching Team Info';
            }
        });
    }
    hideTables() {
        this.showTables = false;
    }

    convertToRows(obj: any): [string, any][] {
        return Object.entries(obj ?? {});
    }
}
