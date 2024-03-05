export function createArrow(source, destination) {
    return arrowLine({
        source: source,
        destination: destination,
        sourcePosition: 'bottomCenter', 
        destinationPosition: 'topCenter', 
        thickness: 1, // Dünne Linie
        style: 'solid', // Solide Linie
        color: '#ffffffde', // Linienfarbe (weiß mit Transparenz)
        endpoint: {
            size: 0.6, 
        },
      
    });
}
