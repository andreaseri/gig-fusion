{{- /*
Return the chart full name
*/ -}}
{{- define "gigfusion.fullname" -}}
{{- if .Release.Name -}}
{{ .Release.Name }}
{{- else -}}
{{ .Chart.Name }}
{{- end -}}
{{- end -}}

{{- /*
Return serviceAccountName
*/ -}}
{{- define "gigfusion.serviceAccountName" -}}
{{- if .Values.serviceAccount.name }}
{{- .Values.serviceAccount.name -}}
{{- else -}}
{{- printf "sa-%s" .Release.Namespace -}}
{{- end -}}
{{- end -}}

{{- /*
Return the namespace for the release; falls back to "default" if missing
*/ -}}
{{- define "gigfusion.namespace" -}}
{{- if .Release.Namespace }}
{{- .Release.Namespace -}}
{{- else -}}
default
{{- end -}}
{{- end -}}