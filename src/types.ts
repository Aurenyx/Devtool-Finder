export type Tool={id:number;name:string;description:string;category:string;languages:string[];domains:string[];experience_level:string[];features:string[];project_types:string[];databases:string[];pricing_type:string;license_type:string;website:string;strengths:string[];limitations:string[];popularity:string};
export type Profile={language:string;domain:string;experience_level:string;project_type:string;database_preference:string;required_features:string[];custom_requirements:string;limit:number};
export type Recommendation={tool:Tool;relevance_score:number;explanations:string[]};
