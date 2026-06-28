import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Component, inject } from "@angular/core";

@Component({
    selector: 'app-summary',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './summary.component.html',
    styleUrl: './summary.component.css'
})
export class SummaryComponent {
  private http = inject(HttpClient);

  base = 'http://localhost:8000';

  summary: any = null;
  summaryError: string | null = null;

  keys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }


  loadSummary(): void {
    this.summaryError = null;
    this.summary = null;

    const url = `${this.base}/summary`;

    this.http.get<any>(url).subscribe({
      next: (res) => {
        const payload = res?.data ?? res;
        if (payload && typeof payload === 'object') {
          this.summary = payload;
        } else {
          this.summaryError = 'Unexpected response format';
        }
      },
      error: (err) => {
        this.summaryError = err?.error?.detail ?? 'Error fetching summary';
      }
    });
  }
  hideSummary(): void {
    this.summary = null;
  }
}