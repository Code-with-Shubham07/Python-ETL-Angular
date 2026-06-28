import { CommonModule } from '@angular/common';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-country-leagues',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './country-leagues.component.html',
  styleUrls: ['./country-leagues.component.css']
})
export class CountryLeaguesComponent {

  base = 'http://localhost:8000';

  countryIdQuery: string = '';
  countryNameQuery: string = '';

  countryError: string | null = null;
  showTable = false;

  countryName: string | null = null;
  leagues: string[] = [];

  constructor(private http: HttpClient) {}

  searchCountry(): void {
    this.countryError = null;
    this.showTable = false;
    this.countryName = null;
    this.leagues = [];

    const id = this.countryIdQuery.trim();
    const name = this.countryNameQuery.trim();

    if (!id && !name) {
      this.countryError = 'Please enter either Country ID or Country Name.';
      return;
    }

    if (id && !/^-?\d+$/.test(id)) {
      this.countryError = 'Country ID must be an integer.';
      return;
    }

    if (id && Number(id) <= 0) {
      this.countryError = 'Country ID must be a positive integer.';
      return;
    }

    if (!id && /^\d+$/.test(name)) {
      this.countryError = 'Country Name must be a valid string.';
      return;
    }

    let params = new HttpParams();

    if (id) {
      params = params.set('country_id', id);
    } else {
      params = params.set('country_name', name);
    }

    this.http.get<any>(`${this.base}/countries/leagues`, { params }).subscribe({
      next: (res) => {
        if (!res || !res.data) {
          this.countryError = 'Unexpected response from server.';
          return;
        }

        this.countryName = res.data.country_name;
        this.leagues = res.data.leagues || [];
        this.showTable = true;
      },
      error: (err) => {
        this.countryError = err?.error?.detail ?? 'Error fetching Country / League Info';
      }
    });
  }

  hideTable(): void {
    this.showTable = false;
  }
}
