import { Routes } from '@angular/router';
import { CountryLeaguesComponent } from './country-leagues/country-leagues.component';
import { PlayerInfoComponent } from './player-info/player-info.component';
import { SummaryComponent } from './summary/summary.component';
import { TeamGoalsComponent } from './team-goals/team-goals.component';
import { TeamInfoComponent } from './team-info/team-info.component';

export const routes: Routes = [
    { path: '', redirectTo: 'summary', pathMatch: 'full' },
    { path: 'summary', component: SummaryComponent },
    { path: 'team-info', component: TeamInfoComponent},
    { path: 'player-info', component: PlayerInfoComponent},
    { path: 'country-leagues', component: CountryLeaguesComponent},
    { path: 'team-goals', component: TeamGoalsComponent}
 
];
