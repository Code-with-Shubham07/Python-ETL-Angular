import { CommonModule } from "@angular/common";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Component } from "@angular/core";
import { FormsModule } from "@angular/forms";

@Component({
    selector: 'app-player-info',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './player-info.component.html',
    styleUrls: ['./player-info.component.css']
})
export class PlayerInfoComponent {
    base = 'http://localhost:8000';

    playerIdQuery: string = '';
    playerNameQuery: string = '';

    playerError: string | null = null;
    showTable = false;

    playerData: any = null;

    constructor(private http: HttpClient) {}

    searchPlayer(): void {
        this.playerError = null;
        this.showTable = false;
        this.playerData = null;

        const id = this.playerIdQuery.trim();
        const name = this.playerNameQuery.trim();

         if (!id && !name) {
            this.playerError = 'Please enter either Player ID or Player Name.';
            return;
        }

        if (id && !/^-?\d+$/.test(id)) {
            this.playerError = 'Player ID must be an integer.';
            return;
        }

        if (id && Number(id) <= 0) {
            this.playerError = 'Player ID must be a positive integer.';
            return;
        }

        if (!id && /^\d+$/.test(name)) {
            this.playerError = 'Player Name must be a valid string.';
            return;
        }

        let params = new HttpParams();

        if (id) {
            params = params.set('player_id', id);
        } else {
            params = params.set('player_name', name);
        }

        this.http.get<any>(`${this.base}/players`, { params }).subscribe({
            next: (res) => {
                if (!res || !res.data) {
                    this.playerError = 'Unexpected response from server.';
                    return;
                }

                this.playerData = res.data;
                this.showTable = true;
            },
            error: (err) => {
                this.playerError = err?.error?.detail ?? 'Error fetching Player Info';
            }
        });
    }

    hideTable(): void {
        this.showTable = false;
    }

    convertToRows(obj: any): [string, any][] {
        return Object.entries(obj ?? {});
    }
}
