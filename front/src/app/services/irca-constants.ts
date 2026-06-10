/**
 * IRCA Water Quality Risk Index Constants
 * 
 * Mirrors backend constants from app/core/constants.py
 * Defines risk level thresholds for water quality classification.
 */

export enum IRCARiskLevel {
  NO_RISK = 'SIN RIESGO',
  LOW = 'BAJO',
  MEDIUM = 'MEDIO',
  HIGH = 'ALTO',
  UNSANITARY = 'INVIABLE SANITARIAMENTE'
}

export interface IRCARiskInfo {
  level: IRCARiskLevel;
  color: string;
  backgroundColor: string;
  threshold: number;
  description: string;
}

/**
 * IRCA risk thresholds based on Colombian water quality standards
 * Reference: Decree 1575 of 2007
 */
export class IRCARiskThresholds {
  static readonly UNSANITARY = 80;  // > 80: Not safe for consumption
  static readonly HIGH = 35;        // > 35: High risk
  static readonly MEDIUM = 14;      // > 14: Medium risk
  static readonly LOW = 5;          // > 5: Low risk
  // <= 5: No risk - water is safe

  /**
   * Get risk level classification from IRCA numeric value
   */
  static getRiskLevel(ircaValue: number): IRCARiskLevel {
    if (ircaValue > this.UNSANITARY) {
      return IRCARiskLevel.UNSANITARY;
    } else if (ircaValue > this.HIGH) {
      return IRCARiskLevel.HIGH;
    } else if (ircaValue > this.MEDIUM) {
      return IRCARiskLevel.MEDIUM;
    } else if (ircaValue > this.LOW) {
      return IRCARiskLevel.LOW;
    }
    return IRCARiskLevel.NO_RISK;
  }

  /**
   * Get complete risk information including colors and description
   */
  static getRiskInfo(ircaValue: number): IRCARiskInfo {
    const level = this.getRiskLevel(ircaValue);
    
    const riskInfoMap: Record<IRCARiskLevel, Omit<IRCARiskInfo, 'level'>> = {
      [IRCARiskLevel.NO_RISK]: {
        color: '#28a745',
        backgroundColor: '#d4edda',
        threshold: 0,
        description: 'Agua segura para consumo humano'
      },
      [IRCARiskLevel.LOW]: {
        color: '#17a2b8',
        backgroundColor: '#d1ecf1',
        threshold: this.LOW,
        description: 'Riesgo bajo - Problemas menores de calidad'
      },
      [IRCARiskLevel.MEDIUM]: {
        color: '#ffc107',
        backgroundColor: '#fff3cd',
        threshold: this.MEDIUM,
        description: 'Riesgo medio - Preocupaciones moderadas'
      },
      [IRCARiskLevel.HIGH]: {
        color: '#fd7e14',
        backgroundColor: '#ffe5d0',
        threshold: this.HIGH,
        description: 'Riesgo alto - Problemas significativos'
      },
      [IRCARiskLevel.UNSANITARY]: {
        color: '#dc3545',
        backgroundColor: '#f8d7da',
        threshold: this.UNSANITARY,
        description: 'Agua no apta para consumo humano'
      }
    };

    return {
      level,
      ...riskInfoMap[level]
    };
  }

  /**
   * Get color for chart/map visualization
   */
  static getColor(ircaValue: number): string {
    return this.getRiskInfo(ircaValue).color;
  }
}

/**
 * API Configuration Constants
 */
export class APIConstants {
  static readonly DEFAULT_PAGE_SIZE = 50;
  static readonly MAX_PAGE_SIZE = 100;
  static readonly DEFAULT_YEAR_START = 2020;
  static readonly DEFAULT_YEAR_END = 2024;
}
