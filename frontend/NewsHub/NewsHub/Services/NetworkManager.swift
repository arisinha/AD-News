import Foundation

enum NetworkError: LocalizedError {
    case invalidURL
    case invalidResponse
    case unauthorized
    case serverError(String)
    case decodingError
    case noData
    case connectionError(String)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "URL inválida"
        case .invalidResponse:
            return "Respuesta inválida del servidor"
        case .unauthorized:
            return "No autorizado. Por favor inicia sesión nuevamente"
        case .serverError(let message):
            return message
        case .decodingError:
            return "Error al procesar la respuesta"
        case .noData:
            return "No se recibieron datos"
        case .connectionError(let message):
            return "Error de conexión: \(message)"
        }
    }
}

class NetworkManager {
    static let shared = NetworkManager()
    
    private let baseURL = AppConfig.baseURL
    
    private init() {}
    
    func request<T: Decodable>(
        endpoint: String,
        method: String = "GET",
        body: Encodable? = nil,
        requiresAuth: Bool = true
    ) async throws -> T {
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 30 // 30 second timeout for slower endpoints
        
        // Add auth token if required
        if requiresAuth, let token = UserDefaults.standard.string(forKey: "auth_token") {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        // Add body if present
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        // Make the request with connection error handling
        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await URLSession.shared.data(for: request)
        } catch let urlError as URLError {
            switch urlError.code {
            case .timedOut:
                throw NetworkError.connectionError("La solicitud tardó demasiado. Intenta de nuevo.")
            case .notConnectedToInternet:
                throw NetworkError.connectionError("No hay conexión a internet")
            case .cannotConnectToHost, .cannotFindHost:
                throw NetworkError.connectionError("No se pudo conectar al servidor")
            default:
                throw NetworkError.connectionError(urlError.localizedDescription)
            }
        } catch {
            throw NetworkError.connectionError(error.localizedDescription)
        }
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            do {
                let decoder = JSONDecoder()
                return try decoder.decode(T.self, from: data)
            } catch {
                print("Decoding error: \(error)")
                throw NetworkError.decodingError
            }
        case 401:
            throw NetworkError.unauthorized
        case 400...499:
            if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw NetworkError.serverError(errorResponse.detail)
            }
            throw NetworkError.serverError("Error del cliente")
        case 500...599:
            throw NetworkError.serverError("Error del servidor")
        default:
            throw NetworkError.invalidResponse
        }
    }
}

struct ErrorResponse: Codable {
    let detail: String
}
