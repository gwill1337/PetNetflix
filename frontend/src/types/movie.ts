
export interface movieCard {
    image: string;
    movieId: number;
    userId: number | null;
    rating: number;
    isFavorite: boolean;
}

export interface MovieDetailsType {
    movie_id: number;
    image?: string;
    title?: string;
    name?: string;
    description?: string;
    rating?: number;
    year?: string | number;
}

export interface Movie {
  movie_id: number;
  name: string;
  title: string;
  image: string;
  rating: number;
  year: string;
}