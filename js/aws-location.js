/**
 * AWS Location Service Integration Module
 * Utiliza chamadas REST com API Key para Geocodificação e Roteirização.
 */

window.AWSLocation = {
  // Configurações e credenciais
  config: {
    region: 'us-east-2',
    apiKey: 'v1.public.eyJqdGkiOiI0NWI1NTAwYS1kN2M3LTRlNDUtODM0YS00NWRjNjBiZjFiYzkifaI91O8DE8edoQZD2Fe4bcjsOYu0PE9Q0nbP7wODg6Ph9Sp5WftL9VL5E1en4f0EEyq_hGJgaBro-Y14jtPlLJZYCR-WB8vqtmzVKzaMpoo5frfbUeM6bEDnz0DOMsRQNovOA_1Wu1AMmFFqeM_zFu3zmerknKnLfv8H4e-i4bZSAroyVzAqEPQeyraiB7KuCXjDjWCAnw659mnRXWRkSRoCOYq1mafb7ehglwdKR7zpG2ZC0p3RSeRmK6z3fqUihR7pkXy430QBwZ0_rOFeyGL6qP_SpMc3DGQygpjrqAflRnYfO-zGDL6P9kyf02QPzJ3Iju0MXD_5pUbnuL2Xekk.NjAyMWJkZWUtMGMyOS00NmRkLThjZTMtODEyOTkzZTUyMTBi',
    placeIndexName: 'indice-lugares-general',
    routeCalculatorName: 'calculadora-rotas-general',
    mapName: 'mapa-estatico-general'
  },

  /**
   * Gera a URL dinâmica para o mapa estático da ocorrência.
   * Utiliza AWS Location Service v2 (Resource-less).
   * @param {number} lat - Latitude
   * @param {number} lng - Longitude
   * @returns {string} - URL da imagem do mapa
   */
  getStaticMapUrl(lat, lng) {
    if (!lat || !lng) return '';
    const zoom = 15;
    const width = 800;
    const height = 400;
    
    return `https://maps.geo.${this.config.region}.api.aws/v2/static/map?center=${lng},${lat}&zoom=${zoom}&width=${width}&height=${height}&key=${encodeURIComponent(this.config.apiKey)}`;
  },

  /**
   * Geocodifica um endereço (texto) para coordenadas [lat, lng].
   * Utiliza AWS Location Service v2 (Resource-less).
   * @param {string} text - Endereço (ex: "Curitiba, PR")
   * @returns {Promise<Array>} - Retorna [lat, lng]
   */
  async geocode(text) {
    if (!text || text.trim() === '') return null;

    const url = `https://places.geo.${this.config.region}.api.aws/v2/geocode?key=${encodeURIComponent(this.config.apiKey)}`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          QueryText: text,
          MaxResults: 1
        })
      });

      if (!response.ok) {
        if (response.status === 403) {
          console.error('AWS Location API Key inválida.');
        }
        throw new Error(`AWS Geocode Error: ${response.statusText}`);
      }

      const data = await response.json();
      if (data.ResultItems && data.ResultItems.length > 0) {
        // AWS v2 retorna Position como [Longitude, Latitude] direto no item
        const point = data.ResultItems[0].Position;
        if (point && point.length === 2) {
          return [point[1], point[0]]; // Retornar [Lat, Lng]
        }
      }
      
      return null;
    } catch (error) {
      console.error('Falha na geocodificação:', error);
      return null;
    }
  },

  /**
   * Calcula a rota entre duas coordenadas [lat, lng].
   * Utiliza AWS Location Service v2 (Resource-less).
   * @param {Array} origin - Coordenadas [lat, lng]
   * @param {Array} destination - Coordenadas [lat, lng]
   * @returns {Promise<Object>} - Distância, tempo e polyline geometry
   */
  async calculateRoute(origin, destination) {
    if (!origin || !destination) return null;

    const url = `https://routes.geo.${this.config.region}.api.aws/v2/routes?key=${encodeURIComponent(this.config.apiKey)}`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          Origin: [origin[1], origin[0]],
          Destination: [destination[1], destination[0]],
          TravelMode: "Truck",
          DistanceUnit: "Kilometers",
          LegGeometryFormat: "Simple"
        })
      });

      if (!response.ok) {
        throw new Error(`AWS Route Error: ${response.statusText}`);
      }

      const data = await response.json();
      
      if (data.Routes && data.Routes.length > 0) {
        const route = data.Routes[0];
        let geometry = [];
        
        // Se a AWS retornou a geometria da perna, converta de [Lng, Lat] para [Lat, Lng]
        if (route.Legs && route.Legs.length > 0 && route.Legs[0].Geometry && route.Legs[0].Geometry.LineString) {
           geometry = route.Legs[0].Geometry.LineString.map(coord => [coord[1], coord[0]]);
        }
        
        // A API v2 retorna a distância em metros por padrão na maioria dos casos.
        let dist = route.Summary.Distance;
        if (dist > 5000) {
          dist = dist / 1000;
        }

        return {
          distanceKm: dist,
          durationSeconds: route.Summary.Duration,
          geometry: geometry
        };
      }
      return null;
    } catch (error) {
      console.error('Falha na roteirização AWS:', error);
      return null;
    }
  }
};
