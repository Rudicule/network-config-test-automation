#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <map>
#include <cctype>

bool isValidIPv4(const std::string& ip) {
    std::stringstream ss(ip);
    std::string segment;
    int count = 0;

    while (std::getline(ss, segment, '.')) {
        count++;

        if (segment.empty()) {
            return false;
        }

        for (char c : segment) {
            if (!std::isdigit(static_cast<unsigned char>(c))) {
                return false;
            }
        }

        int value = std::stoi(segment);

        if (value < 0 || value > 255) {
            return false;
        }
    }

    return count == 4;
}

bool isValidPort(const std::string& portString) {
    try {
        int port = std::stoi(portString);
        return port >= 1 && port <= 65535;
    } catch (...) {
        return false;
    }
}

bool isValidProtocol(const std::string& protocol) {
    return protocol == "http" || protocol == "https";
}

bool isValidTimeout(const std::string& timeoutString) {
    try {
        int timeout = std::stoi(timeoutString);
        return timeout >= 1 && timeout <= 300;
    } catch (...) {
        return false;
    }
}

bool hasRequiredFields(
    const std::map<std::string, std::string>& config
) {
    return config.count("server") &&
           config.count("port") &&
           config.count("protocol") &&
           config.count("timeout");
}

bool validateConfiguration(
    const std::map<std::string, std::string>& config
) {
    if (!hasRequiredFields(config)) {
        return false;
    }

    return isValidIPv4(config.at("server")) &&
           isValidPort(config.at("port")) &&
           isValidProtocol(config.at("protocol")) &&
           isValidTimeout(config.at("timeout"));
}

int main(int argc, char* argv[]) {

    if (argc != 2) {
        std::cerr
            << "Usage: network_validator.exe <config_file>"
            << std::endl;

        return 1;
    }

    std::ifstream file(argv[1]);

    if (!file.is_open()) {
        std::cerr
            << "Error: Could not open configuration file."
            << std::endl;

        return 1;
    }

    std::map<std::string, std::string> config;
    std::string line;

    while (std::getline(file, line)) {

        if (line.empty()) {
            continue;
        }

        size_t delimiter = line.find('=');

        if (delimiter == std::string::npos) {
            continue;
        }

        std::string key = line.substr(0, delimiter);
        std::string value = line.substr(delimiter + 1);

        config[key] = value;
    }

    if (validateConfiguration(config)) {
        std::cout << "VALID" << std::endl;
        return 0;
    }

    std::cout << "INVALID" << std::endl;
    return 2;
}